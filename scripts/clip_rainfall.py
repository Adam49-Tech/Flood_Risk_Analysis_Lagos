import geopandas as gpd
import rasterio
from rasterio.mask import mask
import json
# Paths
shapefile_path = "data/raw/Lagos_boundary.shp"
rainfall_path = "data/raw/rainfall.tif"
output_path = "data/processed/Lagos_rainfall.tif"
# Load Lagos boundary
lagos = gpd.read_file(shapefile_path)
# Clip function
def clip_raster(raster_path, shapefile, output_path):
    with rasterio.open(raster_path) as src:
        geojson = [json.loads(shapefile.to_json())['features'][0]['geometry']]
        out_image, out_transform = mask(src, geojson, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)
    print(f"Clipped rainfall raster saved at {output_path}")
clip_raster(rainfall_path, lagos, output_path)