# --- visualization.py ---

import folium
import os
import config

MAPS_FOLDER = config.MAPS_FOLDER

def save_polygon_map(coords_original, coords_corrected, filename: str):
    """
    Generate and save a folium map with the original and corrected polygons.
    
    Args:
        coords_original (list of tuple): List of (latitude, longitude) points of the original polygon.
        coords_corrected (list of tuple): List of (latitude, longitude) points of the corrected polygon.
        filename (str): Name of the output HTML file to save the map.

    Returns:
        None
    """

    # Calculate map center
    lat_center = (sum(p[0] for p in coords_original) + sum(p[0] for p in coords_corrected)) / (2 * len(coords_original))
    lon_center = (sum(p[1] for p in coords_original) + sum(p[1] for p in coords_corrected)) / (2 * len(coords_original))

    # Initialize folium map
    m = folium.Map(location=[lat_center, lon_center], zoom_start=18)

    # Draw original polygon (red)
    folium.Polygon(
        coords_original,
        color="red",
        weight=2,
        fill=True,
        fill_color="red",
        fill_opacity=0.3,
        tooltip="Original Polygon"
    ).add_to(m)

    # Draw corrected polygon (green)
    folium.Polygon(
        coords_corrected,
        color="green",
        weight=2,
        fill=True,
        fill_color="green",
        fill_opacity=0.3,
        tooltip="Corrected Polygon"
    ).add_to(m)

    # Calculate centroids
    centroid_original = (
        sum([p[0] for p in coords_original]) / len(coords_original),
        sum([p[1] for p in coords_original]) / len(coords_original)
    )

    centroid_corrected = (
        sum([p[0] for p in coords_corrected]) / len(coords_corrected),
        sum([p[1] for p in coords_corrected]) / len(coords_corrected)
    )

    # Add markers for centroids
    folium.Marker(
        location=[centroid_original[0], centroid_original[1]],
        popup="Original centroid",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    folium.Marker(
        location=[centroid_corrected[0], centroid_corrected[1]],
        popup="Corrected centroid",
        icon=folium.Icon(color="green", icon="ok-sign")
    ).add_to(m)

    # Create folder if not exists
    if not os.path.exists(MAPS_FOLDER):
        os.makedirs(MAPS_FOLDER)

    # Save the map to an HTML file
    filepath = os.path.join(MAPS_FOLDER, filename)
    m.save(filepath)
