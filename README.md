# Correction Polygon App

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-brightgreen)
![Render](https://img.shields.io/badge/Hosted%20on-Render-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

🚀 Простое и эффективное API для коррекции координат полигонов с помощью обученной модели машинного обучения.

---

## 📚 Описание

Это приложение принимает полигон (в системе координат SC63 или WGS84),  
вычисляет центроид, предсказывает коррекцию через обученную модель,  
и возвращает:

- Новый центроид полигона
- Предсказанную дельту смещения
- Новый пересчитанный полигон

Реализация построена на основе **FastAPI** и задеплоено на **Render**.

---

## 🌐 Демо

Документация API доступна здесь:  
🔝 [https://correction-polygon-app.onrender.com/docs](https://correction-polygon-app.onrender.com/docs)

---

## 🚀 Быстрый старт локально

```bash
# Клонировать репозиторий
git clone https://github.com/ayri77/correction_polygon_app.git
cd correction_polygon_app

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📦 Структура проекта

```
correction_polygon_app/
│
├── app/
│   └── main.py           # Основной сервер FastAPI
│
├── model/
│   └── model.pkl         # Обученная модель коррекции
│
├── utils/
│   ├── coords.py         # Пересчёт координат SC63 → WGS84
│   ├── features.py       # Генерация признаков
│   ├── parser.py         # Парсинг входных данных
│
├── requirements.txt      # Зависимости проекта
├── Procfile              # Конфигурация для Render
└── README.md             # Документация проекта
```

---

## ✨ Технологии

- Python 3.11
- FastAPI
- Uvicorn
- Scikit-learn
- Numpy
- Shapely
- Pandas
- Render (хостинг)

---

## 🛠 Возможности для улучшения

- Обработка пакетных запросов (Batch API)
- Построение карты изменений через Folium
- Логирование и мониторинг запросов
- Авторизация пользователей (по API-ключу)

---

## 📜 Лицензия

MIT License

## 📬 Контакты

- Email: [pborisov77@gmail.com](mailto:pborisov77@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/pavlo-borysov-45067071](https://www.linkedin.com/in/pavlo-borysov-45067071)
- GitHub: [https://github.com/ayri77](https://github.com/ayri77)

---
