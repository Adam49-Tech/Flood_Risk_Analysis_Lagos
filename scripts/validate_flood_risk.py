import geopandas as gpd
import rasterio
from rasterio.transform import rowcol
import numpy as np
import os
# Paths
raster_path = "data/processed/flood_risk_normalized.tif"  # Your flood risk raster
flood_points_path = "data/validation/flood_points.shp"    # Validation points
# Load flood points
flood_points = gpd.read_file(flood_points_path)
# Reproject points to match raster CRS
with rasterio.open(raster_path) as src:
    raster_crs = src.crs
    raster_data = src.read(1)
    raster_transform = src.transform
    nodata = src.nodata
    width, height = src.width, src.height
flood_points = flood_points.to_crs(raster_crs)
# Validate points inside raster bounds
valid_points = []
values = []
for geom in flood_points.geometry:
    x, y = geom.x, geom.y
    try:
        row, col = rowcol(raster_transform, x, y)
        if (0 <= row < height) and (0 <= col < width):
            val = raster_data[row, col]
            if val != nodata:  # Skip NoData pixels
                valid_points.append((x, y))
                values.append(val)
    except Exception:
        continue
# Convert values to numpy array
values = np.array(values)
# Print summary
print(f"Total validation points: {len(flood_points)}")
print(f"Valid points inside raster: {len(valid_points)}")
if len(values) > 0:
    print(f"Flood risk values range: {values.min()} - {values.max()}")
    # Classification: consider >0.6 as high risk
    predicted = (values > 0.6).astype(int)
    actual = np.ones_like(predicted)  # Assume all validation points are actual floods
    # Compute metrics
    from sklearn.metrics import confusion_matrix, precision_score, recall_score
    cm = confusion_matrix(actual, predicted)
    precision = precision_score(actual, predicted)
    recall = recall_score(actual, predicted)
    print("\nConfusion Matrix:\n", cm)
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
else:
    print("No valid points matched the raster extent.")