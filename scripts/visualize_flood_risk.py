import rasterio
import matplotlib.pyplot as plt
# Load flood risk raster
flood_risk_path = "data/processed/flood_risk.tif"
with rasterio.open(flood_risk_path) as src:
    flood_risk = src.read(1)
# Plot
plt.figure(figsize=(10, 6))
risk_plot = plt.imshow(flood_risk, cmap='RdYlBu_r')
plt.colorbar(risk_plot, label="Flood Risk (0 = low, 1 = high)")
plt.title("Flood Risk Map")
plt.axis('off')
plt.show()