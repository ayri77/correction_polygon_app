# model/inference.py

import joblib
import numpy as np
import pandas as pd
from shapely.geometry import Polygon

from utils.coords import sc63_to_wgs84
from utils.features import compute_centroids
from utils.parser import parse_input_data

import config

def load_model(model_path: str):
    model = joblib.load(model_path)
    return model

def predict_centroid_shift(model, centroid_features):
    """
    model: загруженная модель
    centroid_features: np.array признаков центроида
    """
    prediction = model.predict(centroid_features.reshape(1, -1))
    return prediction.flatten()

def process_polygon(raw_polygon, model, input_crs="SC63"):
    """
    Обработка одного полигона: пересчёт координат, вычисление центроида, коррекция через модель.

    Параметры:
    ----------
    raw_polygon : list of (x, y)
        Список точек полигона.
    model : объект модели
        Загруженная модель коррекции.
    input_crs : str
        "SC63" или "WGS84".

    Возвращает:
    ----------
    dict
        {
            "corrected_centroid": (lon, lat),
            "delta": (delta_lon, delta_lat),
            "corrected_polygon": [(lon1, lat1), (lon2, lat2), ...]
        }
    """
    coords_wgs = []
    zones = []

    # Пересчёт координат
    if input_crs == "SC63":
        for x, y in raw_polygon:
            lon, lat, zone = sc63_to_wgs84(x, y)
            coords_wgs.append((lon, lat))
            zones.append(zone)
        zone = zones[0]
    else:
        coords_wgs = raw_polygon
        zone = None

    # Строим полигон
    polygon = Polygon(coords_wgs)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)

    centroid = polygon.centroid
    centroid_lon = centroid.x
    centroid_lat = centroid.y

    # Подготовка признаков
    if zone is not None:
        centroid_features = np.array([centroid_lon, centroid_lat, zone])
    else:
        centroid_features = np.array([centroid_lon, centroid_lat])

    # Применяем модель
    delta_lon, delta_lat = predict_centroid_shift(model, centroid_features)

    # Корректируем центроид
    corrected_centroid_lon = centroid_lon + delta_lon
    corrected_centroid_lat = centroid_lat + delta_lat

    # Корректируем все точки полигона
    corrected_coords = [(lon + delta_lon, lat + delta_lat) for lon, lat in coords_wgs]

    return {
        "corrected_centroid": (corrected_centroid_lon, corrected_centroid_lat),
        "delta": (delta_lon, delta_lat),
        "corrected_polygon": corrected_coords
    }