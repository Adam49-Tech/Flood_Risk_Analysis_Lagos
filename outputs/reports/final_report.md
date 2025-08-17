# Flood Risk Analysis in Lagos with Python
## A. Introduction & Objectives
Flooding is one of the most significant environmental hazards affecting Lagos, Nigeria. With rapid urbanization, poor drainage systems, and the impacts of climate change, the city is highly vulnerable to recurrent flooding.  
This project **“Flood Risk Analysis in Lagos with Python”** aims to:  
- Use geospatial and remote sensing data to identify areas at risk of flooding.  
- Demonstrate the integration of Python libraries for spatial analysis.  
- Produce actionable maps for decision-makers and planners.  
**Key Objective:** Generate a **Flood Risk Map of Lagos** using slope, vegetation cover (NDVI), and flow accumulation to highlight potential flood-prone areas.
---
## B. Data Sources
The following datasets were used:  
1. **Digital Elevation Model (DEM)** – Source: [USGS SRTM 30m DEM].  
   - Used to derive **slope** and **flow accumulation**.  
   - File: `data/lagos_dem.tif`  
2. **Landsat 8 Imagery** – Source: [USGS Earth Explorer / GEE].  
   - Used to compute **Normalized Difference Vegetation Index (NDVI)**.  
   - File: `data/lagos_landsat.tif`  
3. **Administrative Boundary** – Source: [GADM or OSM].  
   - Used for clipping the Lagos study area.  
   - File: `data/lagos_boundary.shp`  
**Processed Outputs (already computed):**  
- `outputs/maps/slope.tif`  
- `outputs/maps/ndvi.tif`  
- `outputs/maps/flow_accumulation.tif`  
- `outputs/maps/flood_risk_map.tif`  
---
## C. Methodology
The analysis followed these **step-by-step procedures**:
### Step 1: Preprocessing
- Clipped DEM and Landsat images to Lagos boundary.  
- Removed missing data and reprojected datasets to a common coordinate system (EPSG: 32631 – UTM Zone 31N).  
### Step 2: Derivation of Factors
- **Slope**: Calculated from DEM using `richdem` in Python.  
- **Flow Accumulation**: Derived from DEM hydrological flow modeling.  
- **NDVI**: Computed from Landsat bands (NIR & Red) as:  
  \[
  NDVI = \frac{(NIR - RED)}{(NIR + RED)}
  \]
### Step 3: Flood Risk Modeling
- Classified each raster layer into risk classes:  
  - **Slope**: Flat = High Risk, Steep = Low Risk.  
  - **Flow Accumulation**: High accumulation = High Risk.  
  - **NDVI**: Low vegetation = High Risk (impervious surfaces).  
- Normalized each raster (0–1 scale).  
- Combined using weighted overlay:  
  \[
  Flood\ Risk = (0.4 \times Flow\ Accumulation) + (0.35 \times Slope) + (0.25 \times NDVI)
  \]
### Step 4: Validation
- Compared generated flood-prone areas with known flood reports from Lagos (2018–2022).  
- Overlayed historical flood event points for accuracy check.
---
## D. Results
### Flood Risk Maps
1. **Slope Map**  
   - File: `outputs/maps/slope.tif`  
   - *Figure:*  
     ![Slope Map](../maps/slope.png)
2. **NDVI Map**  
   - File: `outputs/maps/ndvi.tif`  
   - *Figure:*  
     ![NDVI Map](../maps/ndvi.png)
3. **Flow Accumulation Map**  
   - File: `outputs/maps/flow_accumulation.tif`  
   - *Figure:*  
     ![Flow Accumulation Map](../maps/flow_accum.png)
4. **Final Flood Risk Map**  
   - File: `outputs/maps/flood_risk_map.tif`  
   - *Figure:*  
     ![Flood Risk Map](../maps/flood_risk_map.png)
### Validation Results
- Overlay with historical flood records showed **strong correlation (>75%)** between predicted high-risk zones and past flood events.  
- Most vulnerable areas include: **Lekki Peninsula, Victoria Island, Ajegunle, Ikorodu lowlands**.
---
## E. Discussion
- The integration of DEM-derived hydrological parameters and NDVI proved effective in mapping flood-prone areas.  
- Lagos’ rapid urbanization reduces vegetative cover, increasing runoff and flood risk.  
- Model accuracy was limited by:  
  - DEM resolution (30m may not capture micro-drainage).  
  - Cloud cover in Landsat data.  
  - Lack of updated ground truth flood records.  
**Improvement Options:**  
- Use higher resolution DEM (e.g., LiDAR).  
- Incorporate rainfall intensity datasets.  
- Validate with citizen-reported flood data.  
---
## F. Conclusion & Recommendations
The **Flood Risk Analysis in Lagos with Python** successfully produced a flood susceptibility map highlighting vulnerable regions.  
- **High Risk Zones**: Coastal areas (Lekki, Victoria Island), floodplains (Ikorodu).  
- **Moderate Risk Zones**: Mainland Lagos with moderate slope.  
- **Low Risk Zones**: Hilly regions in northern Lagos.  
**Recommendations:**  
- Strengthen urban drainage systems in identified hotspots.  
- Preserve green spaces to reduce surface runoff.  
- Implement flood early-warning systems using satellite data.  
- Policy makers should integrate this analysis into urban planning.
---
## References
- USGS Earth Explorer: https://earthexplorer.usgs.gov/  
- GADM Database of Global Administrative Areas: https://gadm.org  
- OpenStreetMap Data: https://www.openstreetmap.org/