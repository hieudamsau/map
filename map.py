import geopandas as gpd
import json

gdf = gpd.read_file("ne_10m_admin_0_countries.shp")

filtered_gdf = gdf[gdf['SOVEREIGNT'].isin(['Vietnam', 'Malaysia', 'United States of America'])]

colors = {
    'Vietnam': '#DA291C',
    'Malaysia': '#00205B',
    'United States of America': '#3C3B6E'
}

geojson = json.loads(filtered_gdf.to_json())

for feature in geojson['features']:
    country = feature['properties']['SOVEREIGNT']
    if country in colors:
        feature['properties']['fill'] = colors[country]         
        feature['properties']['stroke'] = "#000000"              
        feature['properties']['stroke-width'] = 1                
        feature['properties']['fill-opacity'] = 0.7              

# Ghi ra file GeoJSON mới
with open("output_with_style.geojson", "w") as f:
    json.dump(geojson, f, indent=4)

print("✅ Đã thêm màu sắc vào GeoJSON!")
