import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np
import os
def match_paster(src_array, src_profile, match_profile):
    """Reprojects and resamples src_array to match match_profile."""
    # Ensure input is 2D
    if src_array.ndim == 3 and src_array.shape[0] == 1:
        src_array = src_array[0]
    dest_array = np.empty((match_profile['height'], match_profile['width']), dtype=src_array.dtype)
    
    reproject(
        source=src_array,
        destination=dest_array,
        src_transform=src_profile['transform'],
        src_crs=src_profile['crs'],
        dst_transform=match_profile['transform'],
        dst_crs=match_profile['crs'],
        resampling=Resampling.bilinear
    )
    return dest_array
# Paths
slope_path = "data/processed/slope_normalized.tif"
flow_path = "data/processed/flow_accum_normalized.tif"
ndvi_path = "data/processed/ndvi.tif"
# Read slope
with rasterio.open(slope_path) as src:
    slope = src.read(1)
    slope_profile = src.profile
# Read flow accumulation
with rasterio.open(flow_path) as src:
    flow_accum = src.read(1)
    flow_profile = src.profile
# Read NDVI
with rasterio.open(ndvi_path) as src:
    ndvi = src.read()
    ndvi_profile = src.profile
# Match NDVI and flow to slope's resolution and extent
ndvi = match_paster(ndvi, ndvi_profile, slope_profile)
flow_accum = match_paster(flow_accum, flow_profile, slope_profile)
# Define weights (example)
slope_w, flow_w, ndvi_w = 0.3, 0.5, 0.2
# Flood risk model
flood_risk = (slope_w * slope) + (flow_w * flow_accum) + (ndvi_w * ndvi)
# Save
out_path = "data/processed/flood_risk.tif"
out_profile = slope_profile
out_profile.update(dtype=rasterio.float32, count=1)
with rasterio.open(out_path, 'w', **out_profile) as dst:
    dst.write(flood_risk.astype(rasterio.float32), 1)
print(f"Flood risk map saved to {out_path}")