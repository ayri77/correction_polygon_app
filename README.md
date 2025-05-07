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

