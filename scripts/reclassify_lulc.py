import rasterio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Force interactive backend
import matplotlib.pyplot as plt
# Paths
input_lulc_path = "data/processed/Lagos_LULC.tif"  # or data/raw/LULC.tif if clipped in GEE
output_lulc_path = "data/processed/Lagos_LULC_reclassified.tif"
# LULC reclassification map
lulc_risk = {
    10: 0.1,  # Tree cover
    20: 0.2,  # Shrubland
    30: 0.3,  # Grassland
    40: 0.5,  # Cropland
    50: 0.9,  # Built-up
    60: 0.8,  # Bare land
    80: 0.1,  # Water bodies
    90: 0.4,  # Wetlands
    95: 0.2,  # Mangroves
    100: 0.2  # Moss/Lichen
}
# Read LULC raster
with rasterio.open(input_lulc_path) as src:
    lulc = src.read(1)
    profile = src.profile
# Apply reclassification
lulc_reclass = np.zeros_like(lulc, dtype=float)
for key, value in lulc_risk.items():
    lulc_reclass[lulc == key] = value
# Update profile for float32
profile.update(dtype=rasterio.float32)
# Save reclassified raster
with rasterio.open(output_lulc_path, 'w', **profile) as dst:
    dst.write(lulc_reclass.astype(rasterio.float32), 1)
print(f"Reclassified LULC saved at {output_lulc_path}")
print("Unique values after reclassification:", np.unique(lulc_reclass))
# Visualize
plt.figure(figsize=(8,6))
plt.imshow(lulc_reclass, cmap='YlOrRd')
plt.colorbar(label='Flood Risk from LULC')
plt.title("LULC Reclassified for Flood Risk")
plt.show(block=True)