"""
scripts/weighted_overlay_update.py
Weighted overlay (7 layers) + classification.
- Reference raster (for CRS/transform/shape): data/processed/Lagos_DEM.tif
- Inputs (expected in data/processed/):
    Lagos_dem_normalized.tif  (optional)
    Lagos_rainfall_normalized.tif
    Lagos_lulc_normalized.tif
    Lagos_population_normalized.tif
    ndvi.tif
    slope_normalized.tif
    flow_accum_normalized.tif
Outputs:
- data/processed/flood_risk_normalized.tif       (float32, 0-1)
- data/processed/Lagos_FloodRisk_Classification.tif  (uint8: 0 nodata, 1 low, 2 medium, 3 high)
Run:
    python scripts\weighted_overlay_update.py
"""
import os
import sys
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
# ---------- CONFIG ----------
processed = "data/processed"
ref_raster = os.path.join(processed, "Lagos_DEM.tif")  # reference for alignment & profile
# Layer filenames (must exist in data/processed). Edit weights below as you like.
layers = {
    "Lagos_dem_normalized.tif": 0.10,        # elevation influence (optional - can be small)
    "Lagos_rainfall_normalized.tif": 0.28,   # rainfall - high influence
    "Lagos_lulc_normalized.tif": 0.15,       # land cover
    "Lagos_population_normalized.tif": 0.15,# population density
    "ndvi.tif": 0.07,                        # NDVI (vegetation; inverse relation)
    "slope_normalized.tif": 0.12,            # slope
    "flow_accum_normalized.tif": 0.13        # flow accumulation
}
# ----------------------------
# Ensure processed folder exists
os.makedirs(processed, exist_ok=True)
# Helper: full path for a layer name
def p(fn): return os.path.join(processed, fn)
# Check reference raster exists
if not os.path.exists(ref_raster):
    print(f"ERROR: reference raster not found: {ref_raster}")
    sys.exit(1)
# Open reference and get profile, CRS, transform, shape
with rasterio.open(ref_raster) as ref:
    ref_profile = ref.profile.copy()
    ref_crs = ref.crs
    ref_transform = ref.transform
    ref_width = ref.width
    ref_height = ref.height
    # read reference array to detect nodata mask
    ref_arr = ref.read(1)
    ref_nodata = ref.nodata
# Create a mask of valid pixels from reference (True where valid)
if ref_nodata is not None:
    valid_mask = (ref_arr != ref_nodata)
else:
    valid_mask = ~np.isnan(ref_arr)
# Function to load, reproject/resample to reference, and return numpy array (float32) with NaN for nodata
def load_and_match(fn):
    fp = p(fn)
    if not os.path.exists(fp):
        raise FileNotFoundError(f"Missing input layer: {fp}")
    with rasterio.open(fp) as src:
        arr = src.read(1).astype(np.float32)
        src_nodata = src.nodata
        # convert source nodata to NaN
        if src_nodata is not None:
            arr = np.where(arr == src_nodata, np.nan, arr)
        else:
            # keep NaNs if present
            arr = np.where(np.isfinite(arr), arr, np.nan)
        # if already matches ref shape/transform/crs, return
        if (src.crs == ref_crs) and (src.transform == ref_transform) and (src.width == ref_width) and (src.height == ref_height):
            return arr
        # otherwise reproject/resample to reference grid
        dest = np.empty((ref_height, ref_width), dtype=np.float32)
        reproject(
            source=arr,
            destination=dest,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=ref_transform,
            dst_crs=ref_crs,
            resampling=Resampling.bilinear,
            src_nodata=np.nan,
            dst_nodata=np.nan
        )
        return dest
# Min-max normalize array to 0..1 (NaNs remain NaN)
def minmax_norm(a):
    if np.all(np.isnan(a)):
        return a
    a_min = np.nanmin(a)
    a_max = np.nanmax(a)
    if a_max == a_min:
        return np.zeros_like(a)
    out = (a - a_min) / (a_max - a_min)
    out = np.clip(out, 0.0, 1.0)
    # convert NaN remain NaN
    return out
# Load layers, normalize if needed and build weighted sum
print("Loading and processing layers...")
arrays = {}
for name, w in layers.items():
    print(f" - {name} (weight {w}) ...", end="")
    arr = load_and_match(name)
    # If file appears already 0..1 (max <=1 and min >=0), keep; else minmax normalize
    arr_max = np.nanmax(arr) if np.any(np.isfinite(arr)) else np.nan
    arr_min = np.nanmin(arr) if np.any(np.isfinite(arr)) else np.nan
    if np.isfinite(arr_max) and arr_max <= 1.0 and np.isfinite(arr_min) and arr_min >= 0.0:
        arr_norm = arr.copy()
    else:
        arr_norm = minmax_norm(arr)
    arrays[name] = arr_norm
    print(" done. (min/max {:.3f}/{:.3f})".format(np.nanmin(arr_norm) if np.any(np.isfinite(arr_norm)) else np.nan,
                                                  np.nanmax(arr_norm) if np.any(np.isfinite(arr_norm)) else np.nan))
# Adjust NDVI treatment: NDVI high vegetation reduces flood risk, so invert NDVI (1 - ndvi)
ndvi_key = "ndvi.tif"
if ndvi_key in arrays:
    arrays[ndvi_key] = 1.0 - arrays[ndvi_key]
# Normalize weights to sum=1
weights = np.array(list(layers.values()), dtype=float)
weights_sum = weights.sum()
if weights_sum <= 0:
    raise ValueError("Sum of weights must be > 0")
weights = weights / weights_sum
# map keys to normalized weights
norm_weights = dict(zip(list(layers.keys()), weights.tolist()))
print("\nUsing normalized weights:")
for k, v in norm_weights.items():
    print(f"  {k}: {v:.3f}")
# Compute weighted overlay
risk = np.zeros((ref_height, ref_width), dtype=np.float32)
for k, w in norm_weights.items():
    arr = arrays[k]
    # treat NaN as 0 contribution in sum (we'll set mask later)
    arr_f = np.nan_to_num(arr, nan=0.0)
    risk += (arr_f * w)
# Ensure result in 0..1 by minmax normalization (safety)
risk = np.clip(risk, 0.0, 1.0)
# Enforce nodata / mask: where reference is invalid, set to 0 and mark as nodata later
risk[np.logical_not(valid_mask)] = np.nan
# Save normalized flood risk raster
out_risk_path = os.path.join(processed, "flood_risk_normalized.tif")
out_profile = ref_profile.copy()
out_profile.update(dtype=rasterio.float32, count=1, nodata=0)
with rasterio.open(out_risk_path, "w", **out_profile) as dst:
    write_arr = np.nan_to_num(risk, nan=0.0).astype(np.float32)
    dst.write(write_arr, 1)
print(f"\nSaved flood risk raster: {out_risk_path}")
# CLASSIFY into 3 classes (Low=1, Medium=2, High=3). 0 for nodata.
class_map = np.zeros_like(risk, dtype=np.uint8)
# thresholds can be adjusted
low_thresh = 0.33
high_thresh = 0.66
class_map[np.isnan(risk)] = 0
class_map[(risk <= low_thresh) & (~np.isnan(risk))] = 1
class_map[((risk > low_thresh) & (risk <= high_thresh))] = 2
class_map[(risk > high_thresh)] = 3
# Save classification
out_class_path = os.path.join(processed, "Lagos_FloodRisk_Classification.tif")
class_profile = ref_profile.copy()
class_profile.update(dtype=rasterio.uint8, count=1, nodata=0)
with rasterio.open(out_class_path, "w", **class_profile) as dst:
    dst.write(class_map.astype(np.uint8), 1)
print(f"Saved classified map: {out_class_path}")
# Quick summary counts
unique, counts = np.unique(class_map, return_counts=True)
summary = dict(zip(unique.tolist(), counts.tolist()))
print("\nClassification counts (value:count):", summary)
print("\nDONE. You can now visualize the new maps or proceed to validation.")