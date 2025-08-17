import rasterio
from rasterio.enums import Resampling
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# Input paths
dem_path = "data/processed/Lagos_DEM_normalized.tif"
rainfall_path = "data/processed/Lagos_rainfall_normalized.tif"
lulc_path = "data/processed/Lagos_LULC_reclassified.tif"
pop_path = "data/processed/Lagos_population_normalized.tif"
output_path = "data/processed/Lagos_FloodRiskMap.tif"
# Weights
weights = {
    "dem": 0.3,
    "rain": 0.3,
    "lulc": 0.2,
    "pop": 0.2
}
# Function to read and resample raster to match a reference
def read_and_resample(path, ref_profile):
    with rasterio.open(path) as src:
        data = src.read(
            out_shape=(
                src.count,
                ref_profile["height"],
                ref_profile["width"]
            ),
            resampling=Resampling.bilinear
        )
        data = data[0]
    return data
# Use DEM as reference grid
with rasterio.open(dem_path) as ref_src:
    ref_profile = ref_src.profile
    ref_data = ref_src.read(1)
# Read and align all layers
dem = ref_data
rain = read_and_resample(rainfall_path, ref_profile)
lulc = read_and_resample(lulc_path, ref_profile)
pop = read_and_resample(pop_path, ref_profile)
# Replace NaN with 0
dem[np.isnan(dem)] = 0
rain[np.isnan(rain)] = 0
lulc[np.isnan(lulc)] = 0
pop[np.isnan(pop)] = 0
# Weighted overlay
flood_risk = (dem * weights["dem"]) + (rain * weights["rain"]) + (lulc * weights["lulc"]) + (pop * weights["pop"])
# Normalize 0–1
min_val = flood_risk.min()
max_val = flood_risk.max()
flood_risk_normalized = (flood_risk - min_val) / (max_val - min_val)
# Save raster
ref_profile.update(dtype=rasterio.float32)
with rasterio.open(output_path, 'w', **ref_profile) as dst:
    dst.write(flood_risk_normalized.astype(rasterio.float32), 1)
print(f"Flood risk map saved at {output_path}")
print("Range:", flood_risk_normalized.min(), "to", flood_risk_normalized.max())
# Visualize
plt.figure(figsize=(10,8))
plt.imshow(flood_risk_normalized, cmap='RdYlBu_r')
plt.colorbar(label='Flood Risk (0–1)')
plt.title("Flood Risk Map - Lagos")
plt.show(block=True)