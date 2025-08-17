import rasterio
import matplotlib.pyplot as plt
import numpy as np
# File paths
slope_path = "data/processed/slope_normalized.tif"
flow_path = "data/processed/flow_accum_normalized.tif"
ndvi_path = "data/processed/ndvi_normalized.tif"
flood_path = "data/processed/flood_risk.tif"
# Function to read raster
def read_raster(path):
    with rasterio.open(path) as src:
        data = src.read(1)
        data = np.where(data == src.nodata, np.nan, data)
    return data
# Load rasters
slope = read_raster(slope_path)
flow = read_raster(flow_path)
ndvi = read_raster(ndvi_path)
flood_risk = read_raster(flood_path)
# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# NDVI
im1 = axes[0, 0].imshow(ndvi, cmap='YlGn')
axes[0, 0].set_title("NDVI (Normalized)")
plt.colorbar(im1, ax=axes[0, 0], fraction=0.046, pad=0.04)
# Slope
im2 = axes[0, 1].imshow(slope, cmap='terrain')
axes[0, 1].set_title("Slope (Normalized)")
plt.colorbar(im2, ax=axes[0, 1], fraction=0.046, pad=0.04)
# Flow Accumulation
im3 = axes[1, 0].imshow(flow, cmap='Blues')
axes[1, 0].set_title("Flow Accumulation (Normalized)")
plt.colorbar(im3, ax=axes[1, 0], fraction=0.046, pad=0.04)
# Flood Risk
im4 = axes[1, 1].imshow(flood_risk, cmap='Reds')
axes[1, 1].set_title("Flood Risk Map")
plt.colorbar(im4, ax=axes[1, 1], fraction=0.046, pad=0.04)
plt.tight_layout()
plt.show()