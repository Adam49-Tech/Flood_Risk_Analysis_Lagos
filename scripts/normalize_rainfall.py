import numpy as np
import rasterio
import matplotlib.pyplot as plt
# Paths
input_rainfall_path = "data/processed/Lagos_rainfall.tif"
output_rainfall_norm_path = "data/processed/Lagos_rainfall_normalized.tif"
# Open rainfall raster
with rasterio.open(input_rainfall_path) as src:
    rainfall = src.read(1).astype(float)  # convert to float
    profile = src.profile
# Calculate min and max (ignore zeros or negative values)
valid_pixels = rainfall[rainfall > 0]
min_val = valid_pixels.min()
max_val = valid_pixels.max()
# Normalize: (value - min) / (max - min)
rainfall_normalized = (rainfall - min_val) / (max_val - min_val)
rainfall_normalized[rainfall_normalized < 0] = 0  # clean negatives
# Update profile
profile.update(dtype=rasterio.float32)
# Save normalized raster
with rasterio.open(output_rainfall_norm_path, 'w', **profile) as dst:
    dst.write(rainfall_normalized.astype(rasterio.float32), 1)
print(f"Normalized rainfall saved at {output_rainfall_norm_path}")
print(f"Original min: {min_val}, max: {max_val}")
print("Normalized range:", rainfall_normalized.min(), "to", rainfall_normalized.max())
# Quick visualization
plt.figure(figsize=(8,6))
plt.imshow(rainfall_normalized, cmap='Blues')
plt.colorbar(label='Normalized Rainfall (0–1)')
plt.title("Normalized Rainfall - Lagos")
plt.show()