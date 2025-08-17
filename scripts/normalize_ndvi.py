import rasterio
import numpy as np
from rasterio.enums import Resampling
from rasterio.warp import reproject
# Paths
ndvi_path = "data/processed/ndvi.tif"
slope_ref_path = "data/processed/slope_normalized.tif"  # reference grid
ndvi_out_path = "data/processed/ndvi_normalized.tif"
# Read NDVI
with rasterio.open(ndvi_path) as src:
    ndvi = src.read(1)
    ndvi_profile = src.profile
# Read reference (slope)
with rasterio.open(slope_ref_path) as ref:
    ref_profile = ref.profile
    ref_shape = (ref.height, ref.width)
    ref_transform = ref.transform
    ref_crs = ref.crs
# Normalize NDVI (0–1 scale, ignoring NaNs)
ndvi_min, ndvi_max = np.nanmin(ndvi), np.nanmax(ndvi)
ndvi_normalized = (ndvi - ndvi_min) / (ndvi_max - ndvi_min)
# Reproject NDVI to match slope
dst_array = np.empty(ref_shape, dtype=np.float32)
reproject(
    source=ndvi_normalized,
    destination=dst_array,
    src_transform=ndvi_profile["transform"],
    src_crs=ndvi_profile["crs"],
    dst_transform=ref_transform,
    dst_crs=ref_crs,
    resampling=Resampling.bilinear
)
# Save output
out_profile = ref_profile.copy()
out_profile.update(dtype=rasterio.float32, count=1)
with rasterio.open(ndvi_out_path, "w", **out_profile) as dst:
    dst.write(dst_array, 1)
print(f"NDVI normalized and saved to {ndvi_out_path}")