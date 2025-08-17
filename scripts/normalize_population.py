import numpy as np
import rasterio
import matplotlib
matplotlib.use('TkAgg')  # Enable interactive plotting
import matplotlib.pyplot as plt
# Paths
input_pop_path = "data/raw/population.tif"  # Change if your file is in processed folder
output_pop_norm_path = "data/processed/Lagos_population_normalized.tif"
# Open population raster
with rasterio.open(input_pop_path) as src:
    pop = src.read(1).astype(float)
    profile = src.profile
# Handle NoData values
pop[pop == src.nodata] = np.nan
# Normalize: scale to 0-1 (ignore NaN)
valid_pixels = pop[~np.isnan(pop)]
min_val = np.nanmin(valid_pixels)
max_val = np.nanmax(valid_pixels)
pop_normalized = (pop - min_val) / (max_val - min_val)
pop_normalized = np.nan_to_num(pop_normalized, nan=0)  # Replace NaN with 0
# Save normalized raster
profile.update(dtype=rasterio.float32)
with rasterio.open(output_pop_norm_path, 'w', **profile) as dst:
    dst.write(pop_normalized.astype(rasterio.float32), 1)
print(f"Normalized population saved at {output_pop_norm_path}")
print("Range after normalization:", pop_normalized.min(), "to", pop_normalized.max())
# Visualize
plt.figure(figsize=(8,6))
plt.imshow(pop_normalized, cmap='OrRd')
plt.colorbar(label='Normalized Population Density (0–1)')
plt.title("Population Density - Lagos (Normalized)")
plt.show(block=True)