from flask import Flask, request, jsonify
import joblib
import json
from pathlib import Path
import traceback

# Paths
ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)
MODEL_PATH = ARTIFACTS_DIR / "model_xgboost.pkl"
MANIFEST_PATH = ARTIFACTS_DIR / "manifest.json"

if MANIFEST_PATH.exists():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)
else:
    manifest = None  # o lanzar error

# Cargar modelo
clf = joblib.load(MODEL_PATH)

# Inicializar app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "API Breast Cancer Model funcionando 🚀"
    })

@app.route("/manifest", methods=["GET"])
def get_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            manifest = json.load(f)
        return jsonify(manifest)
    else:
        return jsonify({"error": "Manifest not found"}), 404
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON recibido"}), 400

        import pandas as pd

        # Detectar si viene un solo registro (dict) o varios (list of dicts)
        if isinstance(data, dict):
            X_input = pd.DataFrame([data])
        elif isinstance(data, list):
            X_input = pd.DataFrame(data)
        else:
            return jsonify({"error": "Formato JSON inválido"}), 400

        # Verificar que todas las columnas requeridas estén presentes
        missing_cols = set(clf.feature_names_in_) - set(X_input.columns)
        if missing_cols:
            return jsonify({"error": f"Faltan columnas: {missing_cols}"}), 400

        # Predicción
        y_pred = clf.predict(X_input)[0]
        y_proba = clf.predict_proba(X_input)[0][1]

        return jsonify({
            "prediction": int(y_pred),
            "probability": float(y_proba)
        })
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "API Breast Cancer Model funcionando 🚀"}), 200

@app.route("/model-info", methods=["GET"])
def model_info():
    return jsonify({
        "model_name": manifest["model_name"],
        "version": manifest["version"],
        "metrics": manifest["metrics"]["test"],
        "framework": manifest["framework"],
        "created_at": manifest["created_at"]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)