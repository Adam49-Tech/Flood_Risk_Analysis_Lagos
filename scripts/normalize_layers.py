import rasterio
import numpy as np
import os
# Input raster paths
input_rasters = {
    "dem": "data/processed/Lagos_DEM.tif",
    "rainfall": "data/processed/Lagos_rainfall.tif",
    "lulc": "data/processed/Lagos_LULC_reclassified.tif",
    "population": "data/processed/Lagos_population.tif"
}
# Output directory
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)
def normalize_raster(input_path, output_path):
    with rasterio.open(input_path) as src:
        arr = src.read(1).astype(float)
        profile = src.profile
        # Mask nodata
        nodata = profile.get('nodata', None)
        if nodata is not None:
            arr[arr == nodata] = np.nan
        # Normalize (min-max)
        min_val, max_val = np.nanmin(arr), np.nanmax(arr)
        norm_arr = (arr - min_val) / (max_val - min_val)
        norm_arr = np.nan_to_num(norm_arr, nan=0.0)
        # Update profile
        profile.update(dtype=rasterio.float32, nodata=0)
        # Save normalized raster
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(norm_arr.astype(rasterio.float32), 1)
        print(f"Normalized raster saved: {output_path}")
# Normalize each layer
for name, path in input_rasters.items():
    output_path = os.path.join(output_dir, f"Lagos_{name}_normalized.tif")
    normalize_raster(path, output_path)