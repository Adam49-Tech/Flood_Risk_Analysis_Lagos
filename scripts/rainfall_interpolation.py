import numpy as np
import geopandas as gpd
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
# Load rainfall points
rainfall_data = gpd.read_file("data/raw/rainfall_points.shp")
x = rainfall_data.geometry.x
y = rainfall_data.geometry.y
values = rainfall_data['rainfall']
# Ordinary Kriging
OK = OrdinaryKriging(x, y, values, variogram_model='spherical')
gridx = np.linspace(min(x), max(x), 100)
gridy = np.linspace(min(y), max(y), 100)
z, ss = OK.execute('grid', gridx, gridy)
plt.imshow(z, origin='lower')
plt.colorbar(label='Rainfall (mm)')
plt.title('Interpolated Rainfall')
plt.show()