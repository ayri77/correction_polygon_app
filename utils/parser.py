# --- parser.py ---

import json

# --- Helper function ---
def parse_multipolygon_coords(coords):
    """
    Extract external contours from multipolygon coordinates.

    Args:
        coords (list): Nested list of multipolygon coordinates.

    Returns:
        list: List of external contours for polygons.
    """
    polygons = []
    for poly_coords in coords:
        if len(poly_coords) > 0:
            polygons.append(poly_coords[0])  # Only the outer contour
    return polygons

# --- Process list of raw JSON polygons ---
def processing_raw_json(raw_json_list):
    """
    Process a list of raw JSON polygon objects to prepare training data.

    Args:
        raw_json_list (list): List of raw JSON objects containing SC63 and WGS84 polygons.

    Returns:
        records (list): List of point dictionaries (SC63 and WGS84).
        errors (list): List of parsing errors.
    """
    records = []
    errors = []

    for idx, item in enumerate(raw_json_list):
        if not isinstance(item, dict):
            print(f"❌ Invalid element #{idx}: {item}")
            continue

        number = item.get("number", f"no_number_{idx}")
        try:
            # --- SC63 block ---
            sc63_raw = item.get("loof_polygon")
            if not sc63_raw:
                raise ValueError("Missing 'loof_polygon' field.")

            sc63_json = json.loads(sc63_raw)
            coords_sc63 = sc63_json.get("coordinates")
            if not coords_sc63:
                raise ValueError("Missing SC63 coordinates.")

            sc63_polygons = parse_multipolygon_coords(coords_sc63)

            # --- WGS84 block ---
            cadastral_raw = item.get("cadastr.live polygon")
            if not cadastral_raw:
                raise ValueError("Missing 'cadastr.live polygon' field.")

            feature_collection = json.loads(cadastral_raw)
            features = feature_collection.get("features")
            if not features or not isinstance(features[0], dict):
                raise ValueError("Missing or invalid 'features' array.")

            geometry_raw = features[0].get("geometry")
            if not geometry_raw or geometry_raw == "null":
                raise ValueError("Missing or invalid 'geometry' field.")

            if isinstance(geometry_raw, str):
                wgs84_geom = json.loads(geometry_raw)
            else:
                wgs84_geom = geometry_raw

            coords_wgs = wgs84_geom.get("coordinates")
            if not coords_wgs:
                raise ValueError("Missing WGS84 coordinates.")

            wgs84_polygons = parse_multipolygon_coords(coords_wgs)

            if len(sc63_polygons) != len(wgs84_polygons):
                raise ValueError("Mismatch between SC63 and WGS84 polygons.")

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
            print(f"❌ Error parsing {number} (#{idx}): {e}")
            errors.append({"number": number, "error": str(e)})

    return records, errors

# --- Process a single polygon for inference ---
def parse_input_data(raw_json: str):
    """
    Parse a single incoming JSON string and prepare a list of points for inference.

    Args:
        raw_json (str): JSON string containing a polygon in SC63 or WGS84.

    Returns:
        points (list of tuple): List of (x, y) points.
        crs (str): 'SC63' or 'WGS84' coordinate system.

    Example:
        points, crs = parse_input_data(raw_json)
    """
    data = json.loads(raw_json)

    # Detect coordinate system
    if "properties" in data and data["properties"].get("coordSys") == "SC63":
        crs = "SC63"
    else:
        crs = "WGS84"

    # Extract coordinates
    if "coordinates" in data:
        coords_raw = data["coordinates"][0][0]  # Assume one polygon
    elif "features" in data and isinstance(data["features"], list):
        feature = data["features"][0]
        geom = json.loads(feature["geometry"])
        coords_raw = geom["coordinates"][0][0]
    else:
        raise ValueError("Invalid data format: coordinates not found.")

    points = [(float(x), float(y)) for x, y in coords_raw]

    return points, crs
