import rasterio
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# Paths
risk_map_path = "data/processed/Lagos_FloodRiskMap.tif"
lagos_boundary_path = "data/raw/Lagos_boundary.shp"
output_path = "data/processed/Lagos_FloodRisk_Classified.tif"
# Read flood risk raster
with rasterio.open(risk_map_path) as src:
    risk = src.read(1)
    profile = src.profile
# Classification logic
classified = np.zeros_like(risk, dtype=np.uint8)
classified[(risk >= 0) & (risk < 0.34)] = 1  # Low Risk
classified[(risk >= 0.34) & (risk < 0.67)] = 2  # Medium Risk
classified[(risk >= 0.67)] = 3  # High Risk
# Save classified raster
profile.update(dtype=rasterio.uint8, nodata=0)  # Fix: nodata for uint8
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(classified, 1)
print(f"Classified flood risk map saved at {output_path}")
# Visualization
colors = ['#ffffcc', '#fd8d3c', '#bd0026']  # Yellow = Low, Orange = Medium, Red = High
labels = ['Low Risk', 'Medium Risk', 'High Risk']
cmap = ListedColormap(colors)
plt.figure(figsize=(10,8))
plt.imshow(classified, cmap=cmap)
plt.colorbar(ticks=[1, 2, 3], label='Flood Risk Level')
plt.clim(1, 3)
# Overlay Lagos boundary
lagos = gpd.read_file(lagos_boundary_path)
lagos.boundary.plot(ax=plt.gca(), color='black', linewidth=1)
plt.title("Classified Flood Risk Map - Lagos")
plt.show(block=True)