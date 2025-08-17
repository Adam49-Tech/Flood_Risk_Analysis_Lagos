import os
import numpy as np
import rasterio
import richdem as rd
# Paths
dem_path = "data/raw/Lagos_DEM.tif"
slope_out = "data/processed/slope.tif"
slope_norm_out = "data/processed/slope_normalized.tif"
flow_accum_out = "data/processed/flow_accum.tif"
flow_norm_out = "data/processed/flow_accum_normalized.tif"
os.makedirs("data/processed", exist_ok=True)
# Load DEM using rasterio
with rasterio.open(dem_path) as src:
    dem_array = src.read(1, masked=True).filled(np.nan)
    profile = src.profile
# Convert to RichDEM object
dem_rd = rd.rdarray(dem_array, no_data=np.nan)
# Compute slope in degrees
slope = rd.TerrainAttribute(dem_rd, attrib='slope_degrees')
# Save slope
profile.update(dtype=rasterio.float32, nodata=np.nan)
with rasterio.open(slope_out, 'w', **profile) as dst:
    dst.write(slope.astype(np.float32), 1)
# Normalize slope
slope_norm = (slope - np.nanmin(slope)) / (np.nanmax(slope) - np.nanmin(slope))
with rasterio.open(slope_norm_out, 'w', **profile) as dst:
    dst.write(slope_norm.astype(np.float32), 1)
print(f"Slope normalized saved to {slope_norm_out}")
# Compute flow accumulation
flow_accum = rd.FlowAccumulation(dem_rd, method='D8')
# Save flow accumulation
with rasterio.open(flow_accum_out, 'w', **profile) as dst:
    dst.write(flow_accum.astype(np.float32), 1)
# Normalize flow accumulation
flow_norm = (flow_accum - np.nanmin(flow_accum)) / (np.nanmax(flow_accum) - np.nanmin(flow_accum))
with rasterio.open(flow_norm_out, 'w', **profile) as dst:
    dst.write(flow_norm.astype(np.float32), 1)
print(f"Flow accumulation normalized saved to {flow_norm_out}")