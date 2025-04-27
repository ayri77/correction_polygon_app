from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from model.inference import load_model, process_polygon
from utils.parser import parse_input_data

import uvicorn

# --- Инициализация FastAPI ---
app = FastAPI(title="Polygon Correction API", version="1.0.0")

# --- Загрузка модели при старте ---
model = load_model("model/model.pkl")  
MODEL_VERSION = "1c.0"

@app.get("/version")
def get_version():
    """
    Версия API и модели.
    """
    return {
        "api_version": "1.0.0",
        "model_version": MODEL_VERSION
    }

# --- Описание формата входных данных ---
class PolygonRequest(BaseModel):
    polygon_json: str = Field(
        ...,
        example="{\"type\": \"MultiPolygon\", \"properties\": {\"coordSys\": \"SC63\"}, \"coordinates\": [[[[1000, 1000], [2000, 1000], [2000, 2000], [1000, 2000], [1000, 1000]]]]}"
    )

# --- Эндпоинт предсказания ---
@app.post("/predict_polygon", responses={
    200: {"description": "Success in correction polygon", "content": {"application/json": {}}},
    400: {"description": "Error in input data", "content": {"application/json": {}}},
})
def predict_polygon(request: PolygonRequest):
    try:
        points, input_crs = parse_input_data(request.polygon_json)
        result = process_polygon(points, model, input_crs=input_crs)

        return {
            "corrected_centroid_lon": float(result["corrected_centroid"][0]),
            "corrected_centroid_lat": float(result["corrected_centroid"][1]),
            "delta_lon": float(result["delta"][0]),
            "delta_lat": float(result["delta"][1]),
            "corrected_polygon": [(float(x), float(y)) for x, y in result["corrected_polygon"]],
            "input_crs": input_crs,
            "model_version": MODEL_VERSION
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
