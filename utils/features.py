# --- features.py ---

import json
import pandas as pd
from shapely.validation import explain_validity
from shapely.geometry import Polygon

from config import MIN_POLYGON_POINTS

def compute_centroids(df_points, fix_invalid=True, log_errors=True):
    """
    Compute centroids for grouped polygon points in both WGS84 and SC63 systems.

    Args:
        df_points (pd.DataFrame): DataFrame containing polygon points grouped by 'number'.
            Must contain columns: ['number', 'wgs84_lon', 'wgs84_lat', 'sc63_x', 'sc63_y'].
        fix_invalid (bool): Attempt to fix invalid polygons using buffer(0).
        log_errors (bool): Log and return encountered geometry errors.

    Returns:
        pd.DataFrame: DataFrame with centroid coordinates.
        (Optional) pd.DataFrame: DataFrame with detected geometry errors (if log_errors=True).
    """
    results = []
    error_log = []

    for number, group in df_points.groupby("number"):
        row = {"number": number}
        error_entry = {"number": number, "wgs84_error": None, "sc63_error": None}

        # --- WGS84 polygon ---
        poly = None
        coords_wgs = list(zip(group["wgs84_lon"], group["wgs84_lat"]))
        if len(coords_wgs) >= MIN_POLYGON_POINTS:
            try:
                poly_wgs = Polygon(coords_wgs)
                if poly_wgs is None:
                    print(f"⚠️ {number} → Polygon WGS is None after creation.")
                elif not poly_wgs.is_valid:
                    print(f"⚠️ {number} → Invalid WGS84 polygon: {explain_validity(poly_wgs)}")
                    if fix_invalid:
                        print(f"🔧 Attempting to fix WGS84 polygon using buffer(0)...")
                        poly_wgs = poly_wgs.buffer(0)
                        if poly_wgs.is_valid:
                            print(f"✅ {number} → WGS84 polygon fixed successfully.")
                        else:
                            print(f"❌ {number} → WGS84 polygon is still invalid after fix.")

                if poly_wgs.is_valid:
                    row["wgs84_centroid_lon"] = round(poly_wgs.centroid.x, 6)
                    row["wgs84_centroid_lat"] = round(poly_wgs.centroid.y, 6)
                else:
                    error_entry["wgs84_error"] = explain_validity(poly_wgs)
            except Exception as e:
                print(f"❌ Error while processing WGS84 for {number}: {e}")

        # --- SC63 polygon ---
        poly = None
        coords_sc = list(zip(group["sc63_x"], group["sc63_y"]))
        if len(coords_sc) >= MIN_POLYGON_POINTS:
            try:
                poly_sc = Polygon(coords_sc)
                if poly_sc is None:
                    print(f"⚠️ {number} → Polygon SC63 is None after creation.")
                elif not poly_sc.is_valid:
                    print(f"⚠️ {number} → Invalid SC63 polygon: {explain_validity(poly_sc)}")
                    if fix_invalid:
                        print(f"🔧 Attempting to fix SC63 polygon using buffer(0)...")
                        poly_sc = poly_sc.buffer(0)
                        if poly_sc.is_valid:
                            print(f"✅ {number} → SC63 polygon fixed successfully.")
                        else:
                            print(f"❌ {number} → SC63 polygon is still invalid after fix.")

                if poly_sc.is_valid:
                    row["sc63_centroid_x"] = round(poly_sc.centroid.x, 2)
                    row["sc63_centroid_y"] = round(poly_sc.centroid.y, 2)
                else:
                    error_entry["sc63_error"] = explain_validity(poly_sc)
            except Exception as e:
                print(f"❌ Error while processing SC63 for {number}: {e}")

        results.append(row)

        if log_errors and (error_entry["wgs84_error"] or error_entry["sc63_error"]):
            error_log.append(error_entry)

    if log_errors:
        return pd.DataFrame(results), pd.DataFrame(error_log)
    else:
        return pd.DataFrame(results)
