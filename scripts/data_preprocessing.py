import geopandas as gpd
# Load full Nigeria shapefile
gdf = gpd.read_file("data/raw/gadm41_NGA_1.shp")
# Check columns
print("Columns:", gdf.columns)
# Preview first rows
print(gdf.head())
# Check unique state names
print("States in file:", gdf['NAME_1'].unique())
# Filter Lagos
lagos = gdf[gdf['NAME_1'] == 'Lagos']
# Confirm row count
print("Rows after filtering:", len(lagos))
# Save Lagos boundary
lagos.to_file("data/raw/Lagos_boundary.shp")
print("Lagos boundary saved successfully!")
import matplotlib.pyplot as plt
# Plot Lagos
lagos.plot(figsize=(6,6), edgecolor='black', color='lightblue')
plt.title("Lagos State Boundary", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()


