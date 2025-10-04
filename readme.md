# Breast Cancer Prediction API 🚀

![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.1.3-orange)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen)

API REST para predecir cáncer de mama usando un modelo XGBoost entrenado.

---  
## Estructura del proyecto  

├── app.py # API Flask  
├── requirements.txt # Dependencias Python  
├── artifacts/ # Modelo y manifest  
│  ├── model_xgboost.pkl  
│  └── manifest.json  
├── Dockerfile  
└── tests/ # Tests automatizados  
---

## Uso con Docker

1. Construir la imagen:

```bash
docker build -t breast_cancer_api:1.0 .
```  
2. Ejecutar el contenedor:
```bash
docker run -p 5000:5000 breast_cancer_api:1.0
```

3. Acceder a la API:
- Health: GET http://127.0.0.1:5000/health
- Información del modelo: GET http://127.0.0.1:5000/model-info
- Predicción: POST http://127.0.0.1:5000/predict con JSON


3. Acceder a los Test:
```bash
pytest tests/test_api.py
```

4. Clonar y correr local
```bash
git clone https://github.com/tu-usuario/breast-cancer-api.git
cd breast-cancer-api
docker build -t breast_cancer_api:1.0 .
docker run -p 5000:5000 breast_cancer_api:1.0
```
