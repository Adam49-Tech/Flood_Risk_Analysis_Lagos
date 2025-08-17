import rasterio
from rasterio import shutil as rio_shutil
input_path = "data/raw/N06E002.SRTML.1.hgt"
output_path = "data/raw/DEM.tif"
# Open HGT and copy to GeoTIFF
with rasterio.open(input_path) as src:
    profile = src.profile
    profile.update(driver='GTiff')  # Change driver to GeoTIFF
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(src.read())
print(f"Converted {input_path} to {output_path}")