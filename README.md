# Correction Polygon App

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-brightgreen)
![Render](https://img.shields.io/badge/Hosted%20on-Render-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

🚀 A simple and efficient API for polygon coordinate correction using a trained machine learning model.

---

## 📚 Description

This application accepts a polygon (in SC63 or WGS84 coordinate systems),  
computes the centroid, predicts correction using a trained model,  
and returns:

- A new centroid of the polygon
- Predicted shift delta
- A new corrected polygon

Built with **FastAPI** and deployed on **Render**.

---

### 🔐 Data Disclaimer

The model was trained on a private dataset of real-world polygon coordinates (SC63 ↔ WGS84).  
Due to data sensitivity, the training set is **not included** in the public repository.  
However, a simplified JSON structure is described, and the API can be tested via the deployed demo.

## 🌐 Demo

API documentation is available here:  
🔝 [https://correction-polygon-app.onrender.com/docs](https://correction-polygon-app.onrender.com/docs)

---

## 🚀 Quick Start (Local)

```bash
# Clone the repository
git clone https://github.com/ayri77/correction_polygon_app.git
cd correction_polygon_app

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📦 Project Structure

```
correction_polygon_app/
├── app/
│   └── main.py           # Main FastAPI server
│
├── model/
│   └── model.pkl         # Trained correction model
│
├── utils/
│   ├── coords.py         # SC63 → WGS84 coordinate transformation
│   ├── features.py       # Feature generation
│   ├── parser.py         # Input data parsing
│   └── visualization.py # Polygon visualization on a map
│
├── requirements.txt      # Project dependencies
├── Procfile              # Render deployment configuration
└── README.md             # Project documentation
```
---
## 🧠 Model Evaluation Summary

After testing multiple models for predicting coordinate corrections (SC63 → WGS84), we selected the best based on Mean Absolute Error (in meters):

| Model       | MAE Lon (m) | MAE Lat (m) | RMSE (°)   | R²         |
|-------------|-------------|-------------|------------|------------|
| LR          | 2.44        | 3.22        | 0.00031    | -0.0017    |
| Ridge       | 2.45        | 3.18        | 0.00031    | -0.0016    |
| Lasso       | 2.43        | 3.18        | 0.00031    | -0.0016    |
| ElasticNet  | 2.44        | 3.19        | 0.00031    | -0.0016    |
| RANSAC      | **2.36**    | **3.12**    | 0.00031    | -0.0016    |
| Poly2 + LR  | 2.43        | 3.17        | 0.00031    | -0.0017    |
| MLP         | 2.83        | 2.69        | 0.00031    | -0.0021    |
| HGB         | 6.20        | 5.92        | 0.00068    | -0.0051    |
| XGB         | 4.93        | 4.84        | 0.00060    | -0.0043    |

📌 **Selected model:** `RANSAC Regressor`
- Best combination of accuracy and robustness
- Resistant to outliers and stable across zones

📎 *Note: R² is not reliable in this case due to small target variance (sub-degree corrections).*

---

## 🔍 RANSAC – Detailed Polygon Evaluation

**Highlights:**

* Median distance to true centroid: **\~0.28m – 0.75m** (vs. 6–13m for baseline)
* Median polygon IoU improved from **\~0.50–0.85 → \~0.94–0.99**
* Some zones improved IoU by **40–60%**

**Example Field:**

* Distance to baseline center: 5.05 m
* Distance to predicted center: 10.26 m
* IoU with baseline: 86.11%
* IoU with prediction: 99.37%

**Zone Summary:**

| Zone | Baseline Dist (m) | Predicted Dist (m) | IoU Baseline | IoU Predicted |
| ---- | ----------------- | ------------------ | ------------ | ------------- |
| 1    | 13.71             | 4.14               | 0.51         | **0.97**      |
| 2    | 10.50             | 1.13               | 0.66         | **0.98**      |
| 3    | 7.94              | 0.75               | 0.81         | **0.98**      |
| 4    | 9.60              | 3.12               | 0.79         | **0.96**      |
| 5    | 7.04              | 0.56               | 0.73         | **0.99**      |
| 6    | 6.68              | 0.94               | 0.92         | **0.98**      |

**Distribution Insights:**

* Baseline polygons had wide error spread; model prediction concentrated near 1.0 IoU.
* Visual distribution clearly shows clustering of predicted IoU around **0.99**, while baseline shows significant variance.

📍 *Visual maps and analytic dashboards are available in the `results` folder and interactive demo.*

📸 **Screenshots added:**

* Map with polygon clusters across Ukraine
  ![image](https://github.com/user-attachments/assets/18e7c2f6-06e4-40fb-ac3f-c6e98909dee6)
* Detailed zoom-in with corrected vs. baseline geometry
  ![image](https://github.com/user-attachments/assets/d7f7f9d8-bfe9-4527-8d6a-44e94318163a)
* Comparison plots: distance errors, IoU distribution, per-zone evaluation
  ![image](https://github.com/user-attachments/assets/7d4962e4-22c2-4eb7-8f40-1510aac2d972)

  ![image](https://github.com/user-attachments/assets/297902ed-1930-4a11-90ff-b3e55c2ec840)

  ![image](https://github.com/user-attachments/assets/d1d3915a-8e91-414b-88e2-b5f56ac4a32b)
  ![image](https://github.com/user-attachments/assets/97a3a130-b476-407a-a2f4-4b7fa307301e)
  ![image](https://github.com/user-attachments/assets/555332b9-cd83-49cc-bc2b-9de3a35a4814)
  ![image](https://github.com/user-attachments/assets/ab8725ac-fbff-4d93-a939-a12d08de459b)

✅ These visuals demonstrate the practical improvement achieved by applying coordinate correction via machine learning.

---

> For additional insight and replication, check out the full training and evaluation pipeline in the `notebooks/` folder (to be added soon).


---

## ✨ Technologies

- Python 3.11
- FastAPI
- Uvicorn
- Scikit-learn
- Numpy
- Shapely
- Pandas
- Folium
- Render (hosting)

---

## 🛠 Potential Improvements

- Batch API request processing (already partially implemented)
- Map visualization (already implemented)
- Request logging and monitoring
- User authorization (via API keys)
- Model retraining pipeline for continuous learning
- Validation for SC63 zone correctness

---

## Example

Input Polygon (SC63):  
![image](https://github.com/user-attachments/assets/f1640c80-bae0-4b8c-9765-f66b7214a66a)

Corrected Polygon (WGS84):  
![image](https://github.com/user-attachments/assets/11b7137a-2bae-49b7-b7dc-c5d0277d6cda)

![image](https://github.com/user-attachments/assets/69582961-e145-4bd8-85ac-344d5f8e2a05)

Try it live: [https://correction-polygon-app.onrender.com/docs#/]


## 📜 License

MIT License

---

## 📬 Contacts

- Email: [pborisov77@gmail.com](mailto:pborisov77@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/pavlo-borysov-45067071](https://www.linkedin.com/in/pavlo-borysov-45067071)
- GitHub: [https://github.com/ayri77](https://github.com/ayri77)

---

