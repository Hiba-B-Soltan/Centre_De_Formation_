# backend/ml_logic.py
import os
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans

# ============================================================
# 1) Chargement du dataset
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "att.L2JHaz4Is_GMV7IkT1b-qO8ET7LOeLr8XgzQ-SmmWZ0.csv"
)

df = pd.read_csv(CSV_PATH)

LEVEL_COLS = ["math_level", "physics_level", "literature_level", "english_level"]
SOFT_COLS = ["communication", "teamwork", "leadership", "problem_solving"]

df[SOFT_COLS] = df[SOFT_COLS].fillna(0)

# ============================================================
# 2) Encodage niveaux A/B/C/D → 0/1/2/3
# ============================================================

enc = OrdinalEncoder(categories=[["D", "C", "B", "A"]] * 4)
df[LEVEL_COLS] = enc.fit_transform(df[LEVEL_COLS])

# ============================================================
# 3) 🔥 Nouveau calcul du niveau global (MODE) — comme le NOTEBOOK
# ============================================================

def row_mode(vals):
    """Retourne la lettre majoritaire comme dans ton notebook."""
    vals = [v for v in vals if pd.notna(v)]
    return pd.Series(vals).mode().iloc[0]

# On récupère les lettres via l'inverse transform
decoded_levels = enc.inverse_transform(df[LEVEL_COLS])

df["overall_letter"] = [
    row_mode(list(row))
    for row in decoded_levels
]

df["global_level"] = df["overall_letter"].map({
    "A": "Level 4",
    "B": "Level 3",
    "C": "Level 2",
    "D": "Level 1"
})

# ============================================================
# 4) Modèle de Classification
# ============================================================

FEATURES = LEVEL_COLS + SOFT_COLS
X = df[FEATURES]
y = df["global_level"]

model = DecisionTreeClassifier(
    max_depth=8,
    class_weight="balanced",
    random_state=42
)
model.fit(X, y)

# ============================================================
# 5) K-Means soft skills
# ============================================================

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["cluster_soft"] = kmeans.fit_predict(df[SOFT_COLS])
cluster_profiles = df.groupby("cluster_soft")[SOFT_COLS].mean().round(2)

# ============================================================
# 5 bis) Régression satisfaction (inchangée)
# ============================================================

try:
    from xgboost import XGBRegressor
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.impute import SimpleImputer

    if "satisfaction" in df.columns:

        y_reg = df["satisfaction"].dropna()

        X_reg = df.loc[y_reg.index].drop(
            columns=[
                "satisfaction",
                "student_id", "enrollment_date",
                "overall_letter", "overall_level_num", "overall_level"
            ] + LEVEL_COLS,
            errors="ignore"
        )

        num_f = X_reg.select_dtypes(include=[np.number]).columns.tolist()
        cat_f = [c for c in X_reg.columns if c not in num_f]

        prep_reg = ColumnTransformer([

            ("num", Pipeline([
                ("imp", SimpleImputer(strategy="median")),
                ("sc", StandardScaler())
            ]), num_f),

            ("cat", Pipeline([
                ("imp", SimpleImputer(strategy="most_frequent")),
                ("oh", OneHotEncoder(handle_unknown="ignore"))
            ]), cat_f)
        ])

        Xtr, Xte, ytr, yte = train_test_split(
            X_reg, y_reg, test_size=0.2, random_state=42
        )

        xgb = Pipeline([
            ("prep", prep_reg),
            ("xgb", XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            ))
        ])

        xgb.fit(Xtr, ytr)
        pred = xgb.predict(Xte)

        print("\n===== XGBOOST REGRESSION REPORT =====")
        print("MAE :", round(mean_absolute_error(yte, pred), 3))
        print("R² :", round(r2_score(yte, pred), 3))
        print("=====================================\n")

    else:
        print("⚠️ Colonne 'satisfaction' absente → régression ignorée.\n")

except Exception as e:
    print("⚠️ XGBoost non exécuté :", e)

# ============================================================
# 6) Conversion note (inchangé)
# ============================================================

def score_to_level(score: float) -> str:
    if score is None:
        return "D"
    if score >= 16:
        return "A"
    elif score >= 12:
        return "B"
    elif score >= 8:
        return "C"
    else:
        return "D"

# ============================================================
# 7) Recommandation dynamique (inchangé)
# ============================================================

def generate_dynamic_recommendation(level, cluster, levels_letters, soft_vals):
    communication, teamwork, leadership, problem_solving = soft_vals

    weaknesses = []
    strengths = []

    for subject, grade in levels_letters.items():
        label = subject.replace("_level", "").capitalize()
        if grade in ["D", "C"]:
            weaknesses.append(label)
        elif grade == "A":
            strengths.append(label)

    soft_map = {
        "Communication": communication,
        "Travail en équipe": teamwork,
        "Leadership": leadership,
        "Résolution de problèmes": problem_solving
    }

    soft_weak = [k for k, v in soft_map.items() if v <= 4]
    soft_strong = [k for k, v in soft_map.items() if v >= 8]

    if level == "Level 4":
        diagnosis = "L’étudiant présente un excellent niveau global avec une maîtrise avancée."
    elif level == "Level 3":
        diagnosis = "L’étudiant possède un niveau satisfaisant avec un bon potentiel d’évolution."
    elif level == "Level 2":
        diagnosis = "L’étudiant présente un niveau moyen nécessitant un accompagnement ciblé."
    else:
        diagnosis = "Le niveau global est faible. Un plan de renforcement structuré est recommandé."
    # --------------------------------------------
    # 🔥 PLAN D'ACTION DYNAMIQUE SELON LE NIVEAU
    # --------------------------------------------
    action_plans = {
        "Level 4": [
            "Maintenir les performances avec un suivi bi-hebdomadaire.",
            "Participer à des ateliers avancés pour approfondir les compétences clés.",
            "Encadrer ou aider d'autres étudiants pour renforcer leadership et communication.",
            "Fixer un objectif personnel d'excellence académique."
        ],
        "Level 3": [
            "Renforcer les matières légèrement en dessous du niveau A.",
            "Effectuer un mini-projet hebdomadaire pour renforcer la compréhension.",
            "Participer à des activités collaboratives pour améliorer le travail en équipe.",
            "Définir 2 objectifs de progression mesurables."
        ],
        "Level 2": [
            "Suivre un module de remise à niveau dans les matières faibles.",
            "Pratiquer des exercices supplémentaires chaque semaine.",
            "Participer à des sessions de tutorat ou groupes d’étude.",
            "Fixer 3 objectifs mesurables et suivre leur évolution."
        ],
        "Level 1": [
            "Suivre un programme intensif de renforcement (4 semaines).",
            "Faire un suivi hebdomadaire avec un formateur.",
            "Participer à des ateliers obligatoires en soft skills.",
            "Revoir les fondamentaux dans chaque matière identifiée comme faible."
        ]
    }

    plan_html = "".join([f"<li>{step}</li>" for step in action_plans[level]])

    cluster_rec = {
        0: "Développer la communication via des ateliers interactifs et exercices d’expression orale.",
        1: "Renforcer la résolution de problèmes à travers des cas pratiques.",
        2: "Stimuler le leadership grâce à des mini-projets.",
        3: "Renforcer progressivement tous les soft skills pour un profil équilibré.",
        4: "Consolider leadership et communication tout en valorisant l’esprit collaboratif."
    }

    html = f"""
    <div class='reco-block'>
        <h5>📘 Diagnostic général — <span class='text-primary'>{level}</span></h5>
        <p>{diagnosis}</p>

        <hr>

        <h6>🟢 Forces identifiées</h6>
        <ul>
            {''.join(f'<li>{s}</li>' for s in strengths) if strengths else '<li>Aucune force notable détectée.</li>'}
            {''.join(f'<li>{s}</li>' for s in soft_strong)}
        </ul>

        <h6>🔴 Axes d'amélioration</h6>
        <ul>
            {''.join(f'<li>{w}</li>' for w in weaknesses)}
            {''.join(f'<li>{w}</li>' for w in soft_weak)}
        </ul>

        <h6>📌 Recommandation personnalisée (Cluster {cluster})</h6>
        <p>{cluster_rec[cluster]}</p>

        <h6>🎯 Plan d’action (4 semaines)</h6>
        <ol>{plan_html}</ol>
    </div>
    """

    return html

# ============================================================
# 8) Fonction finale utilisée par app.py (inchangée)
# ============================================================

def predict_student(data: dict) -> dict:

    levels_letters = {
        "math_level": score_to_level(float(data.get("math_score", 0))),
        "physics_level": score_to_level(float(data.get("physics_score", 0))),
        "literature_level": score_to_level(float(data.get("literature_score", 0))),
        "english_level": score_to_level(float(data.get("english_score", 0))),
    }

    encoded_levels = enc.transform([[
        levels_letters["math_level"],
        levels_letters["physics_level"],
        levels_letters["literature_level"],
        levels_letters["english_level"],
    ]])[0]

    soft_vals = [
        float(data.get("communication", 0)),
        float(data.get("teamwork", 0)),
        float(data.get("leadership", 0)),
        float(data.get("problem_solving", 0)),
    ]

    X_pred = np.hstack([encoded_levels, soft_vals]).reshape(1, -1)

    predicted_level = model.predict(X_pred)[0]
    cluster_soft = int(kmeans.predict([soft_vals])[0])

    recommendation = generate_dynamic_recommendation(
        predicted_level,
        cluster_soft,
        levels_letters,
        soft_vals
    )

    return {
        "predicted_level": predicted_level,
        "cluster_soft": cluster_soft,
        "recommendation": recommendation,
    }
