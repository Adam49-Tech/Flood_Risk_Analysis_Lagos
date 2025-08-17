import geopandas as gpd
import os
# Ensure output directory exists
os.makedirs("data/validation", exist_ok=True)
# Load flood polygons
flood_poly = gpd.read_file("data/raw/validation/Lagos_Flood_Extents.shp")
# Load Lagos boundary (optional clip for safety)
lagos = gpd.read_file("data/raw/Lagos_boundary.shp")
flood_poly = gpd.clip(flood_poly, lagos)
# Reproject to UTM for accurate centroids
flood_poly = flood_poly.to_crs(epsg=32631)
# Compute centroids
flood_poly['geometry'] = flood_poly.geometry.centroid
# Save as points
output_path = "data/validation/flood_points.shp"
flood_poly.to_file(output_path)
print(f"Flood points created: {len(flood_poly)} at {output_path}")