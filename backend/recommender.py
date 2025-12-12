import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

def load_dataset():
    current_dir = Path(__file__).parent
    primary = current_dir / 'etudiants.csv'
    if primary.exists():
        return pd.read_csv(primary)

    data_dir = current_dir / 'data'
    fallback = None
    for name in [
        'att.L2JHaz4Is_GMV7IkT1b-qO8ET7LOeLr8XgzQ-SmmWZ0.csv',
        'students.csv',
        'dataset.csv'
    ]:
        p = data_dir / name
        if p.exists():
            fallback = p
            break

    if fallback is None:
        raise FileNotFoundError(
            f"Dataset introuvable. Ajoutez 'etudiants.csv' à {current_dir} ou un CSV dans {data_dir}."
        )

    return pd.read_csv(fallback)

def create_sample_dataset(path: Path):
    data = {
        'formation': [
            'Développement Web Full Stack',
            'Data Science Avancée',
            'Marketing Digital',
            'Gestion de Projet Agile',
            'Design UX/UI',
            'Cybersécurité',
            'Intelligence Artificielle',
            'Gestion des Ressources Humaines',
            'Communication Digitale',
            'Développement Mobile'
        ],
        'categorie': [
            'Informatique', 'Informatique', 'Marketing', 'Management', 'Design',
            'Informatique', 'Informatique', 'Ressources Humaines', 'Communication', 'Informatique'
        ],
        'difficulte': [3, 4, 2, 3, 3, 4, 5, 2, 2, 3],
        'duree_mois': [6, 9, 4, 3, 5, 8, 10, 3, 4, 6],
        'langue': ['Français', 'Anglais', 'Français', 'Français', 'Français', 
                  'Anglais', 'Anglais', 'Français', 'Français', 'Français'],
        'competences_requises': [
            'HTML,CSS,JavaScript,React,Node.js',
            'Python,Maths,Statistiques,SQL',
            'Marketing,Réseaux Sociaux,Rédaction',
            'Management,Communication,Organisation',
            'Design,UX,UI,Photoshop,Figma',
            'Sécurité,Réseaux,Linux,Python',
            'Python,Maths,ML,Deep Learning',
            'RH,Communication,Droit du travail',
            'Rédaction,Réseaux Sociaux,Marketing',
            'Java,Android,Kotlin,Firebase'
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def calculate_compatibility(profile: Dict, formation_competences: str) -> float:
    # Charger le dataset
    df = load_dataset()
    
    # Calculer la compatibilité basée sur les compétences et les notes
    competences_requises = [c.strip() for c in formation_competences.split(',')]
    compatibilite = 0
    
    # Exemple de logique de correspondance (à adapter selon vos besoins)
    for comp in competences_requises:
        if comp in df.columns:
            # Calculer la moyenne des notes pour la compétence
            if comp in ['math_score', 'physics_score', 'chemistry_score', 'biology_score', 'literature_score', 'english_score']:
                score = df[comp].mean() / 20  # Normaliser entre 0 et 1
                compatibilite += score
            # Ajouter d'autres critères de correspondance si nécessaire
    
    return compatibilite / len(competences_requises) if competences_requises else 0

def get_recommendations(profile: Dict) -> List[Dict]:
    # Charger le dataset
    df = load_dataset()
    
    # Créer une liste des formations uniques basée sur la colonne 'preferred_option'
    formations = df['preferred_option'].unique().tolist()
    
    # Si aucune formation n'est trouvée, utiliser des formations par défaut
    if not formations:
        formations = [
            "Informatique", "Lettres", "Sciences", "Arts", "Commerce", 
            "Ingénierie", "Médecine", "Droit", "Architecture", "Économie"
        ]
    
    # Calculer la compatibilité pour chaque formation
    recommendations = []
    for formation in formations:
        # Ici, vous pouvez ajouter une logique pour déterminer les compétences requises
        # pour chaque formation en fonction de vos besoins
        competences_requises = ",".join([
            'math_score', 'physics_score', 'chemistry_score', 
            'biology_score', 'literature_score', 'english_score'
        ])
        
        score = calculate_compatibility(profile, competences_requises)
        recommendations.append({
            'formation': formation,
            'score': round(score * 100, 2),  # Convertir en pourcentage
            'description': f"Formation en {formation} basée sur votre profil"
        })
    
    # Trier par score décroissant
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations[:5]  # Retourner les 5 meilleures recommandations

_MODEL_CACHE: Dict[str, object] = {}

def _ensure_models():
    if _MODEL_CACHE.get('initialized'):
        return
    df = load_dataset()
    feature_candidates = [
        'math_score', 'physics_score', 'chemistry_score', 'biology_score', 'literature_score', 'english_score',
        'communication', 'teamwork', 'leadership', 'problem_solving',
        'age', 'parent_income', 'attendance_rate'
    ]
    feature_columns = [c for c in feature_candidates if c in df.columns]
    X = df[feature_columns].copy()
    X = X.fillna(X.median(numeric_only=True))
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    le = LabelEncoder()
    y = df['preferred_option'].astype(str).fillna('Unknown')
    y_enc = le.fit_transform(y)
    clf = RandomForestClassifier(random_state=42, n_estimators=200)
    clf.fit(X_scaled, y_enc)
    importances = clf.feature_importances_
    feature_means = X.mean(numeric_only=True)
    fi = sorted([
        {'name': str(feature_columns[i]), 'importance': float(importances[i])}
        for i in range(len(feature_columns))
    ], key=lambda x: x['importance'], reverse=True)
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_scaled)
    centers = kmeans.cluster_centers_.mean(axis=1)
    order = np.argsort(centers)
    labels_map = {}
    labels_map[int(order[0])] = 'faible'
    labels_map[int(order[1])] = 'moyen'
    labels_map[int(order[2])] = 'excellent'
    _MODEL_CACHE['initialized'] = True
    _MODEL_CACHE['df'] = df
    _MODEL_CACHE['feature_columns'] = feature_columns
    _MODEL_CACHE['scaler'] = scaler
    _MODEL_CACHE['label_encoder'] = le
    _MODEL_CACHE['classifier'] = clf
    _MODEL_CACHE['kmeans'] = kmeans
    _MODEL_CACHE['X_scaled'] = X_scaled
    _MODEL_CACHE['cluster_label_map'] = labels_map
    _MODEL_CACHE['feature_importances'] = fi
    _MODEL_CACHE['feature_means'] = {str(k): float(feature_means[k]) for k in feature_means.index}

def get_recommendation_details(profile: Dict) -> Dict:
    _ensure_models()
    df = _MODEL_CACHE['df']
    feature_columns = _MODEL_CACHE['feature_columns']
    scaler: StandardScaler = _MODEL_CACHE['scaler']
    le: LabelEncoder = _MODEL_CACHE['label_encoder']
    clf: RandomForestClassifier = _MODEL_CACHE['classifier']
    kmeans: KMeans = _MODEL_CACHE['kmeans']
    X_scaled = _MODEL_CACHE['X_scaled']
    cluster_label_map = _MODEL_CACHE['cluster_label_map']
    row = {c: profile.get(c, np.nan) for c in feature_columns}
    for c in feature_columns:
        if pd.isna(row[c]):
            median = df[c].median()
            row[c] = median
    df_student = pd.DataFrame([row])
    student_scaled = scaler.transform(df_student)
    proba = clf.predict_proba(student_scaled)[0]
    classes = le.classes_
    option_probabilities = {str(classes[i]): round(float(proba[i] * 100), 2) for i in range(len(classes))}
    best_idx = int(np.argmax(proba))
    recommended_option = str(classes[best_idx])
    cluster_idx = int(kmeans.predict(student_scaled)[0])
    cluster_label = cluster_label_map.get(cluster_idx, str(cluster_idx))
    distances = np.linalg.norm(X_scaled - student_scaled[0], axis=1)
    top_indices = np.argsort(distances)[:10]
    similar_students = df.iloc[top_indices][['student_id', 'preferred_option']].fillna('').to_dict('records')
    parcours = {
        "Engineering": ["Math Avancé", "Physique Appliquée", "Python"],
        "Science": ["Biologie", "Chimie", "Statistiques"],
        "IT": ["Algorithmique", "Développement Web", "Python"],
        "Letters": ["Littérature", "Communication", "Philosophie"],
        "Arts": ["Design", "Créativité", "Histoire de l'art"],
        "Health": ["Biologie", "Anatomie", "Chimie"],
        "Economics": ["Microéconomie", "Business", "Finance"]
    }
    recommended_courses = parcours.get(recommended_option, ["Cours généraux"])
    fi = _MODEL_CACHE.get('feature_importances', [])
    means = _MODEL_CACHE.get('feature_means', {})
    top = fi[:5]
    explanations = [{
        'name': t['name'],
        'importance': round(t['importance'] * 100, 2),
        'student_value': float(df_student.iloc[0][t['name']]) if t['name'] in df_student.columns else None,
        'dataset_mean': means.get(t['name'])
    } for t in top]
    return {
        'recommended_option': recommended_option,
        'recommended_courses': recommended_courses,
        'option_probabilities': option_probabilities,
        'cluster': cluster_label,
        'similar_students': similar_students,
        'explanations': {
            'top_features': explanations
        }
    }

def get_clustered_students() -> List[Dict]:
    _ensure_models()
    df = _MODEL_CACHE['df']
    kmeans: KMeans = _MODEL_CACHE['kmeans']
    X_scaled = _MODEL_CACHE['X_scaled']
    cluster_label_map = _MODEL_CACHE['cluster_label_map']
    if hasattr(kmeans, 'labels_') and len(kmeans.labels_) == len(df):
        cluster_indices = kmeans.labels_
    else:
        cluster_indices = kmeans.predict(X_scaled)
    cluster_labels = [cluster_label_map.get(int(idx), str(idx)) for idx in cluster_indices]
    cols = [
        'student_id', 'age', 'gender', 'region', 'school_type',
        'math_score', 'physics_score', 'literature_score', 'english_score',
        'preferred_option'
    ]
    cols = [c for c in cols if c in df.columns]
    out = df[cols].copy()
    out['cluster'] = cluster_labels
    return out.fillna('').to_dict('records')

def get_exploration_overview() -> Dict:
    _ensure_models()
    df = _MODEL_CACHE['df']
    kmeans: KMeans = _MODEL_CACHE['kmeans']
    X_scaled = _MODEL_CACHE['X_scaled']
    cluster_label_map = _MODEL_CACHE['cluster_label_map']
    if hasattr(kmeans, 'labels_') and len(kmeans.labels_) == len(df):
        cluster_indices = kmeans.labels_
    else:
        cluster_indices = kmeans.predict(X_scaled)
    cluster_labels = [cluster_label_map.get(int(idx), str(idx)) for idx in cluster_indices]
    option_counts = (
        df['preferred_option'].fillna('Unknown').value_counts().reset_index().rename(columns={'index': 'preferred_option', 'preferred_option': 'count'})
    )
    cluster_counts = (
        pd.Series(cluster_labels).value_counts().reset_index().rename(columns={'index': 'cluster', 0: 'count'})
    )
    score_cols = [c for c in ['math_score', 'physics_score', 'literature_score', 'english_score'] if c in df.columns]
    df_tmp = df.copy()
    df_tmp['cluster'] = cluster_labels
    avg_scores_by_cluster = (
        df_tmp.groupby('cluster')[score_cols].mean().reset_index().to_dict('records')
    )
    formations = df['preferred_option'].dropna().unique().tolist()
    return {
        'formations': formations,
        'option_counts': option_counts.to_dict('records'),
        'cluster_counts': cluster_counts.to_dict('records'),
        'avg_scores_by_cluster': avg_scores_by_cluster
    }
