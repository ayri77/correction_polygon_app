import json

# --- Вспомогательная функция ---
def parse_multipolygon_coords(coords):
    """
    Парсинг внешних контуров мультиполигонов.

    Параметры:
    ----------
    coords : list
        Вложенный список координат мультиполигонов.

    Возвращает:
    ----------
    polygons : list
        Список внешних контуров полигонов.
    """
    polygons = []
    for poly_coords in coords:
        if len(poly_coords) > 0:
            polygons.append(poly_coords[0])  # только внешний контур
    return polygons

# --- Функция для обработки списка полигонов ---
def processing_raw_json(raw_json_list):
    """
    Обработать список сырых JSON-объектов для подготовки обучающего датасета.

    Параметры:
    ----------
    raw_json_list : list
        Список JSON-объектов с полигонами SC63 и WGS84.

    Возвращает:
    ----------
    records : list
        Список словарей с точками (SC63 и WGS84).

    errors : list
        Список ошибок обработки.
    """
    records = []
    errors = []

    for idx, item in enumerate(raw_json_list):
        if not isinstance(item, dict):
            print(f"❌ Missing element #{idx}: incorrect record — {item}")
            continue

        number = item.get("number", f"no_number_{idx}")
        try:
            # --- SC63 ---
            sc63_raw = item.get("loof_polygon")
            if not sc63_raw:
                raise ValueError("loof_polygon is missing or null")

            sc63_json = json.loads(sc63_raw)
            coords_sc63 = sc63_json.get("coordinates")
            if not coords_sc63:
                raise ValueError("SC63 coordinates missing")

            sc63_polygons = parse_multipolygon_coords(coords_sc63)

            # --- WGS84 ---
            cadastral_raw = item.get("cadastr.live polygon")
            if not cadastral_raw:
                raise ValueError("cadastr.live polygon is missing or null")

            feature_collection = json.loads(cadastral_raw)
            features = feature_collection.get("features")
            if not features or not isinstance(features[0], dict):
                raise ValueError("features array is missing or not valid")

            geometry_raw = features[0].get("geometry")
            if not geometry_raw or geometry_raw == "null":
                raise ValueError("geometry is missing or invalid")

            if isinstance(geometry_raw, str):
                wgs84_geom = json.loads(geometry_raw)
            else:
                wgs84_geom = geometry_raw

            coords_wgs = wgs84_geom.get("coordinates")
            if not coords_wgs:
                raise ValueError("WGS84 coordinates missing")

            wgs84_polygons = parse_multipolygon_coords(coords_wgs)

            if len(sc63_polygons) != len(wgs84_polygons):
                raise ValueError("Polygon count mismatch")

            for sc63_poly, wgs84_poly in zip(sc63_polygons, wgs84_polygons):
                for i, ((sc_x, sc_y), (lon, lat)) in enumerate(zip(sc63_poly, wgs84_poly)):
                    records.append({
                        "number": number,
                        "sc63_x": sc_x,
                        "sc63_y": sc_y,
                        "wgs84_lon": lon,
                        "wgs84_lat": lat
                    })

        except Exception as e:
            print(f"❌ Error in {number} (#{idx}): {e}")
            errors.append({"number": number, "error": str(e)})

    return records, errors

# --- Функция для обработки одного полигона для инференса ---
def parse_input_data(raw_json: str):
    """
    Распарсить входящий JSON и подготовить массив точек для дальнейшей обработки.

    Параметры:
    ----------
    raw_json : str
        Строка JSON, содержащая полигон в SC63 или WGS84.

    Возвращает:
    ----------
    points : List[Tuple[float, float]]
        Список координат [(x, y), (x, y), ...].

    crs : str
        Строка 'SC63' или 'WGS84', определяющая систему координат.

    Пример:
    -------
    points, crs = parse_input_data(raw_json)
    """
    data = json.loads(raw_json)

    # Определяем систему координат
    if "properties" in data and data["properties"].get("coordSys") == "SC63":
        crs = "SC63"
    else:
        crs = "WGS84"

    # Извлекаем координаты
    if "coordinates" in data:
        coords_raw = data["coordinates"][0][0]  # Для одного полигона
    elif "features" in data and isinstance(data["features"], list):
        feature = data["features"][0]
        geom = json.loads(feature["geometry"])
        coords_raw = geom["coordinates"][0][0]
    else:
        raise ValueError("Неверный формат данных: не найдены координаты")

    points = [(float(x), float(y)) for x, y in coords_raw]

    return points, crs
