import rasterio
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
# Paths
classified_map_path = "data/processed/Lagos_FloodRisk_Classified.tif"
lagos_boundary_path = "data/raw/Lagos_boundary.shp"
output_png = "outputs/Lagos_Flood_Risk_Map.png"
# Read classified raster
with rasterio.open(classified_map_path) as src:
    classified = src.read(1)
# Read Lagos boundary
lagos = gpd.read_file(lagos_boundary_path)
# Define colors and labels
colors = ['#ffffcc', '#fd8d3c', '#bd0026']  # Yellow, Orange, Red
labels = ['Low Risk', 'Medium Risk', 'High Risk']
cmap = ListedColormap(colors)
# Create legend handles
legend_handles = [Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
# Plot map
plt.figure(figsize=(12, 10))
plt.imshow(classified, cmap=cmap)
plt.colorbar(ticks=[1, 2, 3], label='Flood Risk Level')
plt.clim(1, 3)
# Overlay Lagos boundary
lagos.boundary.plot(ax=plt.gca(), color='black', linewidth=1)
# Add title and legend
plt.title("Flood Risk Map - Lagos", fontsize=16, fontweight='bold')
plt.legend(handles=legend_handles, loc='lower left', fontsize=12, frameon=True)
# Save to file
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"Final map exported successfully as {output_png}")