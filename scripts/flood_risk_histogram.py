import rasterio
import matplotlib.pyplot as plt
import numpy as np
# Load flood risk raster
flood_risk_path = "data/processed/flood_risk.tif"
with rasterio.open(flood_risk_path) as src:
    flood_risk = src.read(1)
# Remove NoData values
flood_risk = np.where(flood_risk == src.nodata, np.nan, flood_risk)
flood_risk = flood_risk[~np.isnan(flood_risk)]
# Plot histogram
plt.figure(figsize=(8, 5))
plt.hist(flood_risk, bins=50, color='skyblue', edgecolor='black')
plt.xlabel("Flood Risk Value (0 = low, 1 = high)")
plt.ylabel("Frequency")
plt.title("Flood Risk Value Distribution")
plt.grid(axis='y', alpha=0.7)
plt.show()