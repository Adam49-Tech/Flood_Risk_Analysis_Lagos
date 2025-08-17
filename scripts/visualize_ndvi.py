import rasterio
import matplotlib.pyplot as plt
import numpy as np
# Path to NDVI file
ndvi_path = "data/processed/ndvi.tif"
# Open and read in downsampled mode
with rasterio.open(ndvi_path) as src:
    # Read with resampling to reduce memory load
    ndvi = src.read(
        1,
        out_shape=(
            int(src.height // 4),  # downsample by factor of 4
            int(src.width // 4)
        ),
        resampling=rasterio.enums.Resampling.average
    )
# Mask invalid values
ndvi = np.where((ndvi < -1) | (ndvi > 1), np.nan, ndvi)
# Plot NDVI
plt.figure(figsize=(10, 8))
ndvi_plot = plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(ndvi_plot, label="NDVI")
plt.title("NDVI Map (Downsampled)")
plt.xlabel("Column #")
plt.ylabel("Row #")
plt.tight_layout()
plt.show()