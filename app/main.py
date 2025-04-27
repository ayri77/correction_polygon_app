# --- main.py ---

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from model.inference import load_model, process_polygon
from typing import List, Optional

from utils.parser import parse_input_data
from utils.visualization import save_polygon_map

import uvicorn
import time

# --- Initialize FastAPI ---
app = FastAPI(title="Polygon Correction API", version="1.0.0")

# --- Load model on startup ---
model = load_model("model/model.pkl")
MODEL_VERSION = "1c.0"

@app.get("/version", response_model=dict)
def get_version():
    """
    Returns the API and model version.
    """
    return {
        "api_version": "1.0.0",
        "model_version": MODEL_VERSION
    }

# --- Request schema for single polygon ---
class PolygonRequest(BaseModel):
    polygon_json: str = Field(
        ...,
        example="{\"type\": \"MultiPolygon\", \"properties\": {\"coordSys\": \"SC63\"}, \"coordinates\": [[[[1000, 1000], [2000, 1000], [2000, 2000], [1000, 2000], [1000, 1000]]]]}"
    )
    visualize: Optional[bool] = False

@app.post("/predict_polygon", responses={
    200: {"description": "Successful correction of a polygon"},
    400: {"description": "Invalid input data"},
})
def predict_polygon(request: PolygonRequest):
    """
    Process and correct a single polygon.
    Optionally generate a visualization map.
    """
    try:
        points, input_crs = parse_input_data(request.polygon_json)
        result = process_polygon(points, model, input_crs=input_crs)

        response = {
            "corrected_centroid_lon": float(result["corrected_centroid"][0]),
            "corrected_centroid_lat": float(result["corrected_centroid"][1]),
            "delta_lon": float(result["delta"][0]),
            "delta_lat": float(result["delta"][1]),
            "corrected_polygon": [(float(x), float(y)) for x, y in result["corrected_polygon"]],
            "input_crs": input_crs,
            "model_version": MODEL_VERSION
        }

        if request.visualize:
            filename = f"map_{int(time.time() * 1000)}.html"
            save_polygon_map(result["original_polygon"], result["corrected_polygon"], filename)
            response["map_url"] = f"/maps/{filename}"

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process polygon: {str(e)}")

# --- Request schema for batch polygons ---
class BatchPolygonRequest(BaseModel):
    polygons_json: List[str]
    visualize: Optional[bool] = False

@app.post("/batch_predict_polygons", responses={
    200: {"description": "Successful correction of multiple polygons"},
    400: {"description": "Invalid input data"},
})
def batch_predict_polygons(request: BatchPolygonRequest):
    """
    Process and correct a batch of polygons.
    Returns a list of corrected polygons.
    """
    results = []

    try:
        for polygon_json in request.polygons_json:
            points, input_crs = parse_input_data(polygon_json)
            result = process_polygon(points, model, input_crs=input_crs)

            results.append({
                "corrected_centroid_lon": float(result["corrected_centroid"][0]),
                "corrected_centroid_lat": float(result["corrected_centroid"][1]),
                "delta_lon": float(result["delta"][0]),
                "delta_lat": float(result["delta"][1]),
                "corrected_polygon": [(float(x), float(y)) for x, y in result["corrected_polygon"]],
                "input_crs": input_crs,
                "model_version": MODEL_VERSION
            })

        return results

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process batch polygons: {str(e)}")

# Mount static folder for maps
app.mount("/maps", StaticFiles(directory="maps"), name="maps")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
