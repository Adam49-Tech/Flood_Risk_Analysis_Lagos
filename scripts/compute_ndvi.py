import os
import rasterio
import numpy as np
# Paths
raw_dir = "data/raw"
processed_dir = "data/processed"
# Your existing NDVI file
ndvi_path = os.path.join(raw_dir, "ndvi_lagos.tif")
ndvi_out = os.path.join(processed_dir, "ndvi.tif")
# Read NDVI
with rasterio.open(ndvi_path) as src:
    ndvi_data = src.read(1).astype(np.float32)
    meta = src.meta.copy()
# Optional normalization to 0–1
ndvi_min = np.nanmin(ndvi_data)
ndvi_max = np.nanmax(ndvi_data)
if ndvi_max != ndvi_min:
    ndvi_data = (ndvi_data - ndvi_min) / (ndvi_max - ndvi_min)
# Save normalized NDVI
meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(ndvi_out, 'w', **meta) as dst:
    dst.write(ndvi_data.astype(rasterio.float32), 1)
print(f"NDVI saved to {ndvi_out}")