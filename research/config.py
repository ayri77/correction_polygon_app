# config.py

# Пути
RAW_JSON_PATH = "./mnt/data/numbers_polygons.json"
ERRORS_JSON_PATH = "./mnt/data/errors_geometry_missing.csv"
PROCESSED_CSV_PATH = "./mnt/data/points_processed.csv"
CENTROIDS_CSV_PATH = "./mnt/data/centroids.csv"
CENTROID_ERRORS_CSV_PATH = "./mnt/data/centroid_errors.csv"
RESULTS_DIR = "./mnt/results/"

# Колонки
COORD_COLUMNS = ["sc63_x", "sc63_y"]
TARGET_COLUMNS = ["wgs84_lon", "wgs84_lat"]

# Кадастровый формат
REGION_CODE_LENGTH = 5

# Тестовое разбиение
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Геометрия
MIN_POLYGON_POINTS = 3
ROUND_AREA_SC63 = 2
ROUND_AREA_WGS84 = 2
ROUND_ASPECT_RATIO = 6