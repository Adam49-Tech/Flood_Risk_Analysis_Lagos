# Flood Risk Analysis in Lagos with Python
This project analyzes **flood risk in Lagos, Nigeria** using Python, geospatial datasets, and hydrological analysis techniques.  
It combines elevation data, slope, NDVI, and flow accumulation to identify high-risk flood zones and visualize them in GeoTIFFs and maps.
---
## 📂 Project Structure
```plaintext
Flood-Risk-Analysis-Lagos/
│
├── data/                        # Input datasets
│   ├── lagos_dem.tif            # Digital Elevation Model (DEM) for Lagos
│   ├── lagos_landcover.tif      # Land cover raster
│   ├── lagos_rivers.shp         # Lagos rivers shapefile
│   ├── lagos_boundary.shp       # Lagos boundary shapefile
│   └── README_datasets.md       # Dataset source & description
│
├── results/                     # Output GeoTIFFs and maps
│   ├── slope.tif
│   ├── ndvi.tif
│   ├── flow_accumulation.tif
│   └── flood_risk_map.png
│
├── scripts/                     # Python scripts for analysis
│   ├── generate_slope.py
│   ├── generate_ndvi.py
│   ├── generate_flow_accumulation.py
│   └── flood_risk_analysis.py
│
├── LICENSE                      # License file
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
---
📊 Datasets
The project uses the following datasets:
DEM (Digital Elevation Model): SRTM 30m from USGS Earth Explorer
Landcover Data: Copernicus Global Land Cover
Rivers Shapefile: HydroSHEDS river network
Boundary Data: Lagos shapefile from GADM
Slope (slope.tif) – Represents terrain steepness in degrees.
NDVI (ndvi.tif) – Normalized Difference Vegetation Index, indicating vegetation health.
Flow Accumulation (flow_accumulation.tif) – Shows areas where water is likely to accumulate.
Dataset sources are detailed in data/README_datasets.md.
---
🤝 Contributing
This is a personal project, but you’re welcome to suggest improvements via GitHub Issues or Pull Requests.
---
📌 Author
Adam Joseph Egwu
🌍 Abuja, Nigeria
📧 egwuadam@yahoo.co.uk
Environmental Management MSc, GIS & Remote Sensing Enthusiast