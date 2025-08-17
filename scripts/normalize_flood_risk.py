import rasterio
from rasterio import plot
import numpy as np
# Input and output paths
input_path = "data/processed/Lagos_FloodRiskMap.tif"
output_path = "data/processed/flood_risk_normalized.tif"
with rasterio.open(input_path) as src:
    data = src.read(1)
    profile = src.profile
    # Normalize
    data_min, data_max = np.nanmin(data), np.nanmax(data)
    data_norm = (data - data_min) / (data_max - data_min)
    data_norm = (data_norm * 100).astype(rasterio.float32)
    # Save
    profile.update(dtype=rasterio.float32)
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(data_norm, 1)
print("✅ flood_risk_normalized.tif saved.")