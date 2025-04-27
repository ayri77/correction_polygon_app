# --- inference.py ---

import joblib
import numpy as np
import pandas as pd
from shapely.geometry import Polygon

from utils.coords import sc63_to_wgs84
from utils.features import compute_centroids
from utils.parser import parse_input_data

import config

def load_model(model_path: str):
    """
    Load a correction model from a file.

    Args:
        model_path (str): Path to the saved model file (.pkl).

    Returns:
        model: Loaded model object.
    """
    model = joblib.load(model_path)
    return model

def predict_centroid_shift(model, centroid_features):
    """
    Predict centroid correction using the loaded model.

    Args:
        model: Loaded model object.
        centroid_features (np.ndarray): Feature array of the centroid.

    Returns:
        np.ndarray: Predicted delta (shift) for longitude and latitude.
    """
    prediction = model.predict(centroid_features.reshape(1, -1))
    return prediction.flatten()

def process_polygon(raw_polygon, model, input_crs="SC63"):
    """
    Process a single polygon: reproject coordinates if needed, 
    compute centroid, apply correction via the model.

    Args:
        raw_polygon (list of tuple): List of polygon points (x, y) or (lon, lat).
        model: Loaded correction model.
        input_crs (str): Input coordinate system, "SC63" or "WGS84".

    Returns:
        dict: {
            "corrected_centroid": (corrected_lon, corrected_lat),
            "delta": (delta_lon, delta_lat),
            "corrected_polygon": [(lon1, lat1), (lon2, lat2), ...],
            "original_polygon": [(lon1, lat1), (lon2, lat2), ...]
        }
    """
    coords_wgs = []
    zones = []

    # Reproject coordinates if needed
    if input_crs == "SC63":
        for x, y in raw_polygon:
            lon, lat, zone = sc63_to_wgs84(x, y)
            coords_wgs.append((lon, lat))
            zones.append(zone)
        zone = zones[0]  # Take the first detected zone
    else:
        coords_wgs = raw_polygon
        zone = None

    # Build a polygon
    polygon = Polygon(coords_wgs)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)

    centroid = polygon.centroid
    centroid_lon = centroid.x
    centroid_lat = centroid.y

    # Prepare features for prediction
    if zone is not None:
        centroid_features = np.array([centroid_lon, centroid_lat, zone])
    else:
        centroid_features = np.array([centroid_lon, centroid_lat])

    # Predict centroid shift
    delta_lon, delta_lat = predict_centroid_shift(model, centroid_features)

    # Apply correction to centroid
    corrected_centroid_lon = centroid_lon + delta_lon
    corrected_centroid_lat = centroid_lat + delta_lat

    # Apply correction to polygon points
    corrected_coords = [(lon + delta_lon, lat + delta_lat) for lon, lat in coords_wgs]

    # Debug output (optional, comment out if not needed)
    # print("=== DEBUG POLYGON ===")
    # print(f"Coords WGS after conversion: {coords_wgs}")
    # print(f"Detected SC63 Zone: {zone}")
    # if zone == 0:
    #     print("⚠️ WARNING: SC63 Zone is 0! Coordinate conversion may be incorrect!")

    return {
        "corrected_centroid": (corrected_centroid_lon, corrected_centroid_lat),
        "delta": (delta_lon, delta_lat),
        "corrected_polygon": corrected_coords,
        "original_polygon": coords_wgs
    }
