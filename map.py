import geopandas as gpd
import json

# Đọc dữ liệu
gdf = gpd.read_file("ne_10m_admin_0_countries.shp")

# Lọc các quốc gia cần thiết
filtered_gdf = gdf[gdf['SOVEREIGNT'].isin(['Vietnam', 'Malaysia', 'United States of America', 'Indonesia'])]

# Đặt màu cho từng nước
colors = {
    'Vietnam': '#DA291C',  # Xanh lá cây sáng
    'Malaysia': '#1E90FF',  # Xanh dương
    'United States of America': '#FF4500',  # Đỏ cam
    'Indonesia': '#FFD700'  # Vàng
}

# Chuyển thành GeoJSON (dạng dictionary)
geojson = json.loads(filtered_gdf.to_json())

# Thêm thuộc tính màu vào GeoJSON
for feature in geojson['features']:
    country = feature['properties']['SOVEREIGNT']
    if country in colors:
        feature['properties']['fill'] = colors[country]          # Màu nền
        feature['properties']['stroke'] = "#000000"              # Màu viền
        feature['properties']['stroke-width'] = 1                # Độ dày viền
        feature['properties']['fill-opacity'] = 0.7              # Độ trong suốt của nền

# Ghi ra file GeoJSON mới
with open("output_with_style.geojson", "w") as f:
    json.dump(geojson, f, indent=4)

print("✅ Đã thêm màu sắc vào GeoJSON, bao gồm cả Indonesia!")
