from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from recommender import (
    get_recommendation_details,
    load_dataset as rec_load_dataset,
    get_clustered_students,
    get_exploration_overview,
)

app = Flask(__name__)
CORS(app)

DF_CACHE = None

def load_dataset():
    global DF_CACHE
    if DF_CACHE is not None:
        return DF_CACHE
    try:
        DF_CACHE = rec_load_dataset()
    except Exception:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "data", "att.L2JHaz4Is_GMV7IkT1b-qO8ET7LOeLr8XgzQ-SmmWZ0.csv")
        DF_CACHE = pd.read_csv(csv_path)
    return DF_CACHE

@app.route("/rania", methods=["GET"]) 
def root():
    return jsonify({"message": "Section Rania – API Flask"})

@app.route("/rania/recommend", methods=["POST"]) 
@app.route("/recommend", methods=["POST"]) 
def recommend():
    data = request.get_json() or {}
    try:
        details = get_recommendation_details(data)
        return jsonify(details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rania/formations", methods=["GET"]) 
@app.route("/formations", methods=["GET"]) 
def get_formations():
    try:
        df = load_dataset()
        formations = df["preferred_option"].dropna().unique().tolist()
        return jsonify({"formations": formations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rania/stats", methods=["GET"]) 
@app.route("/stats", methods=["GET"]) 
def get_stats():
    try:
        df = load_dataset()
        total_students = len(df)
        total_formations = df["preferred_option"].nunique()
        average_scores = {
            "math": float(df["math_score"].mean()),
            "physics": float(df["physics_score"].mean()),
            "literature": float(df["literature_score"].mean()),
            "english": float(df["english_score"].mean()),
        }
        formation_stats = (
            df.groupby("preferred_option").agg({
                "student_id": "count",
                "math_score": "mean",
                "physics_score": "mean",
                "literature_score": "mean",
                "english_score": "mean",
            }).rename(columns={"student_id": "count"}).reset_index()
        )
        return jsonify({
            "total_students": total_students,
            "total_formations": total_formations,
            "average_scores": average_scores,
            "formation_stats": formation_stats.to_dict("records"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rania/students", methods=["GET"]) 
@app.route("/students", methods=["GET"]) 
def get_students():
    try:
        df = load_dataset()
        cols = [
            "student_id", "age", "gender", "region", "school_type",
            "math_score", "physics_score", "literature_score", "english_score",
            "preferred_option",
        ]
        students = df[cols].to_dict("records")
        for s in students:
            s["student_name"] = s.get("student_name") or f"Étudiant {s.get('student_id')}"
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rania/students_clusters", methods=["GET"]) 
@app.route("/students_clusters", methods=["GET"]) 
def students_clusters():
    try:
        students = get_clustered_students()
        counts = {}
        for s in students:
            c = s.get("cluster", "Unknown")
            counts[c] = counts.get(c, 0) + 1
        return jsonify({"counts": counts, "students": students})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rania/explore", methods=["GET"]) 
@app.route("/explore", methods=["GET"]) 
def explore():
    try:
        overview = get_exploration_overview()
        return jsonify(overview)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
