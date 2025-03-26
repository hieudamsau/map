import geopandas as gpd
from shapely.geometry import Point, LineString
import json

# Đọc dữ liệu từ file GeoJSON
file_path = 'Hs_converted.geojson'
gdf = gpd.read_file(file_path)

# Kiểm tra và gán CRS nếu thiếu
if gdf.crs is None:
    print("⚠️ CRS không được xác định. Đang gán CRS là EPSG:4326...")
    gdf.set_crs(epsg=4326, inplace=True)
else:
    print(f"✅ CRS hiện tại: {gdf.crs}")

# Trích xuất các tọa độ từ các features
coordinates = []
for feature in gdf['geometry']:
    if feature is None:
        continue
    if feature.geom_type == 'Point':
        coordinates.append((feature.x, feature.y))
    elif feature.geom_type == 'LineString':
        coordinates.extend(list(feature.coords))
    elif feature.geom_type in ['MultiPoint', 'MultiLineString']:
        for geom in feature.geoms:
            coordinates.extend(list(geom.coords))
    elif feature.geom_type in ['Polygon', 'MultiPolygon']:
        for geom in feature.geoms if feature.geom_type == 'MultiPolygon' else [feature]:
            coordinates.extend(list(geom.exterior.coords))

# Kiểm tra xem có dữ liệu không
if len(coordinates) == 0:
    print("❌ Không tìm thấy dữ liệu tọa độ!")
else:
    print(f"✅ Đã trích xuất {len(coordinates)} tọa độ")

    # Tạo đối tượng LineString từ các tọa độ để nối các điểm
    line = LineString(coordinates)

    # ✅ Tạo GeoDataFrame mới chỉ chứa LineString duy nhất
    new_gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")

    # ✅ Ghi đè lên file cũ tạm thời (để xử lý lại với thuộc tính màu)
    temp_file = 'temp.geojson'
    new_gdf.to_file(temp_file, driver='GeoJSON')

    # ✅ Đọc lại file GeoJSON và thêm thuộc tính màu
    with open(temp_file, 'r') as f:
        data = json.load(f)

    for feature in data['features']:
        feature['properties']['stroke'] = "#DA291C"            # Màu đường
        feature['properties']['stroke-width'] = 2              # Độ dày đường
        feature['properties']['stroke-opacity'] = 0.8          # Độ trong suốt của đường
        feature['properties']['fill'] = "#DA291C"              # Màu nền
        feature['properties']['fill-opacity'] = 0.6            # Độ trong suốt của màu nền

    # ✅ Ghi đè lại vào file cũ
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"✅ Đã ghi đè thành công vào file: {file_path}")
