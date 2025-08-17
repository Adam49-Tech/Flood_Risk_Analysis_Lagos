import rasterio
import numpy as np
import os
def normalize_raster(input_path, output_path):
    with rasterio.open(input_path) as src:
        profile = src.profile
        data = src.read(1).astype('float32')
        # Mask NoData values
        nodata = profile.get("nodata", None)
        if nodata is not None:
            mask = (data == nodata)
        else:
            mask = np.isnan(data)
        valid_data = np.ma.masked_array(data, mask=mask)
        # Normalization (min-max)
        min_val = valid_data.min()
        max_val = valid_data.max()
        if max_val - min_val != 0:
            norm_data = (valid_data - min_val) / (max_val - min_val)
        else:
            norm_data = valid_data  # Avoid division by zero
        # Fill NoData areas with original NoData
        norm_data = norm_data.filled(nodata if nodata is not None else np.nan)
        # Save
        profile.update(dtype='float32', compress='lzw')
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(norm_data.astype('float32'), 1)
        print(f"Normalized raster saved to {output_path}")
# Paths
processed_dir = "data/processed"
layers = [
    ("ndvi_lagos.tif", "ndvi_normalized.tif"),
    ("slope.tif", "slope_normalized.tif"),
    ("flow_accumulation.tif", "flow_accum_normalized.tif")
]
for in_file, out_file in layers:
    in_path = os.path.join(processed_dir, in_file)
    out_path = os.path.join(processed_dir, out_file)
    if os.path.exists(in_path):
        normalize_raster(in_path, out_path)
    else:
        print(f"⚠ Skipped: {in_path} not found.")