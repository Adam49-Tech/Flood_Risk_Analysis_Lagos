import numpy as np
import rasterio
from rasterio.plot import show
# Load normalized layers
rainfall = rasterio.open("data/processed/rainfall_norm.tif").read(1)
elevation = rasterio.open("data/processed/elevation_norm.tif").read(1)
population = rasterio.open("data/processed/pop_norm.tif").read(1)
# Weighted sum
risk_index = 0.4 * rainfall + 0.3 * (1 - elevation) + 0.2 * population
np.save("data/processed/flood_risk.npy", risk_index)
# Visualization
import matplotlib.pyplot as plt
plt.imshow(risk_index, cmap='Reds')
plt.colorbar(label='Flood Risk')
plt.title('Flood Risk Index')
plt.show()