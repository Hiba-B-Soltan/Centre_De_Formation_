# backend/app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

from ml_logic import predict_student

app = Flask(__name__, template_folder="templates")
CORS(app)

# Mémoire en RAM pour les prédictions (pour le dashboard)
PREDICTIONS_LOG = []


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Reçoit un JSON du frontend, appelle le modèle
    et renvoie le résultat + log dans PREDICTIONS_LOG.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "JSON body required"}), 400

    try:
        result = predict_student(data)

        # enrichir pour l'admin (on garde aussi une partie des inputs)
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "age": data.get("age"),
            "gender": data.get("gender"),
            "region": data.get("region"),
            "math_score": data.get("math_score"),
            "physics_score": data.get("physics_score"),
            "literature_score": data.get("literature_score"),
            "english_score": data.get("english_score"),
            "communication": data.get("communication"),
            "teamwork": data.get("teamwork"),
            "leadership": data.get("leadership"),
            "problem_solving": data.get("problem_solving"),
            "predicted_level": result["predicted_level"],
            "cluster_soft": result["cluster_soft"],
            "recommendation": result["recommendation"],
        }
        PREDICTIONS_LOG.append(log_entry)

        # LOG console lisible
        print("\n📥 ========= FRONTEND → BACKEND =========")
        print(f"Payload reçu : {data}")
        print("📤 ========= BACKEND → FRONTEND =========")
        print(f"Résultat envoyé : {result}")
        print("========================================\n")

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Dashboard admin ----------

@app.route("/admin", methods=["GET"])
def admin_page():
    """
    Renvoie la page HTML du dashboard admin.
    """
    return render_template("admin.html")


@app.route("/admin_data", methods=["GET"])
def admin_data():
    """
    Renvoie toutes les prédictions loggées pour le dashboard.
    """
    return jsonify(PREDICTIONS_LOG)


if __name__ == "__main__":
    # serveur dev
    app.run(host="0.0.0.0", port=5000, debug=True)
