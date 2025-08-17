import numpy as np
import rasterio
# Load normalized layers
layers = [
    rasterio.open("data/processed/elevation_normalized.tif").read(1),
    rasterio.open("data/processed/slope_normalized.tif").read(1),
    rasterio.open("data/processed/ndvi_normalized.tif").read(1),
    rasterio.open("data/processed/lulc_normalized.tif").read(1),
    rasterio.open("data/processed/flow_accum_normalized.tif").read(1),
    rasterio.open("data/processed/Lagos_population.tif").read(1)
]
# Assign weights
weights = [0.2, 0.1, 0.1, 0.2, 0.2, 0.2]
# Weighted sum
flood_risk = sum(w * l for w, l in zip(weights, layers))
# Save raster
with rasterio.open("data/processed/elevation_normalized.tif") as src:
    meta = src.meta.copy()
meta.update({
    "dtype": rasterio.float32,
    "count": 1
})
with rasterio.open("data/processed/flood_risk_normalized.tif", "w", **meta) as dst:
    dst.write(flood_risk.astype(rasterio.float32), 1)
# Save PNG
import matplotlib.pyplot as plt
plt.imshow(flood_risk, cmap='RdYlBu_r')
plt.colorbar(label="Flood Risk (0-1)")
plt.title("Flood Risk Map - Lagos")
plt.axis("off")
plt.savefig("outputs/Lagos_Flood_Risk_Map.png", bbox_inches="tight", dpi=300)