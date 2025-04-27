import json
import numpy as np
from utils.parser import parse_input_data, processing_raw_json
from model.inference import process_polygon

# Заглушка модели
class DummyModel:
    def predict(self, X):
        return np.array([[0.0001, 0.0001]])

dummy_model = DummyModel()

# Загрузка реальных данных
with open("mnt/data/numbers_polygons.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Тест 1. Много полигонов SC63
print("\n=== Тест: Много полигонов SC63 ===")
records, errors = processing_raw_json(raw_data)
if errors:
    print(f"Ошибок при парсинге: {len(errors)}")
else:
    print(f"Успешно распарсено записей: {len(records)}")

# Можно сгруппировать по номеру и прогонять по одному полигону

# Тест 2. Один полигон SC63
print("\n=== Тест: Один полигон SC63 ===")
test_sc63_json = json.dumps({
    "type": "MultiPolygon",
    "properties": {"coordSys": "SC63"},
    "coordinates": [[[[1000, 1000], [2000, 1000], [2000, 2000], [1000, 2000], [1000, 1000]]]]
})
points, crs = parse_input_data(test_sc63_json)
corrected = process_polygon(points, dummy_model, input_crs=crs)
print("Корректированный центроид (SC63):", corrected)

# Тест 3. Один полигон WGS84
print("\n=== Тест: Один полигон WGS84 ===")
test_wgs_json = json.dumps({
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": json.dumps({
            "type": "MultiPolygon",
            "coordinates": [[[[23.0, 49.0], [23.1, 49.0], [23.1, 49.1], [23.0, 49.1], [23.0, 49.0]]]]
        })
    }]
})
points, crs = parse_input_data(test_wgs_json)
corrected = process_polygon(points, dummy_model, input_crs=crs)
print("Корректированный центроид (WGS84):", corrected)
