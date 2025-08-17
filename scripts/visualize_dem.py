import rasterio
import matplotlib.pyplot as plt
dem_path = "data/processed/Lagos_DEM.tif"
with rasterio.open(dem_path) as src:
    dem = src.read(1)
plt.figure(figsize=(8,6))
plt.imshow(dem, cmap='terrain')
plt.colorbar(label='Elevation (m)')
plt.title("Lagos DEM")
plt.show()
print("DEM Stats:")
print("Min:", dem.min(), "Max:", dem.max(), "Mean:", dem.mean())