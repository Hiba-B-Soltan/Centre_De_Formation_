# 🎓 Centre de Formation Intelligent
### Prédiction, Segmentation et Recommandation des Parcours d'Apprenants par Machine Learning

Un projet de Machine Learning appliqué visant à transformer les données brutes d'un centre de formation (académiques, comportementales et satisfaction) en **décisions actionnables** : prédire la réussite, segmenter les profils, et recommander des parcours personnalisés.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Classification-EA4C89)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Méthodologie](https://img.shields.io/badge/Méthodologie-CRISP--DM-blueviolet)
![License](https://img.shields.io/badge/status-projet%20académique-lightgrey)

---

## 📋 Table des matières

- [Contexte & Vision](#-contexte--vision)
- [Objectifs du projet](#-objectifs-du-projet)
- [Architecture des 3 axes ML](#-architecture-des-3-axes-ml)
- [Répartition par binôme](#-répartition-par-binôme)
- [Dataset](#-dataset)
- [Stack technique](#-stack-technique)
- [Méthodologie CRISP-DM](#-méthodologie-crisp-dm)
- [Structure du projet](#-structure-du-projet)
- [Installation](#-installation)
- [Pipeline d'exécution](#-pipeline-dexécution)
- [Métriques d'évaluation](#-métriques-dévaluation)
- [Exemple concret](#-exemple-concret)
- [Livrables](#-livrables)
- [Roadmap](#-roadmap)
- [Contact](#-contact)

---

## 🎯 Contexte & Vision

Un centre de formation dispose d'un volume croissant de données sur ses apprenants — profils démographiques, parcours académiques, compétences comportementales (soft skills) et retours de satisfaction — sans réellement les exploiter.

**Vision du projet :** faire passer le centre d'une gestion *réactive* à une gestion *prédictive et personnalisée*, en s'appuyant sur trois piliers du Machine Learning :

> 🔮 **Prédire** la réussite et la trajectoire des apprenants
> 🧩 **Segmenter** les profils pour mieux comprendre les populations
> 🎯 **Recommander** des actions concrètes et individualisées

---

## 🎯 Objectifs du projet

**Objectif global :** prédire la réussite des apprenants, segmenter leurs profils, et recommander des actions pour améliorer leur expérience de formation.

Le projet est structuré en **9 objectifs ML** (3 objectifs × 3 binômes), couvrant l'ensemble du parcours apprenant : de la performance académique à la satisfaction globale.

---

## 🧠 Architecture des 3 axes ML

| Axe | Type de problème | Algorithmes envisagés |
|---|---|---|
| 🔮 **Prédiction** | Classification supervisée | Logistic Regression, Random Forest, SVM, XGBoost |
| 🧩 **Segmentation** | Clustering non-supervisé | K-Means, DBSCAN, ACP (réduction de dimension / visualisation) |
| 🎯 **Recommandation** | Filtrage & règles métier | Filtrage basé contenu (similarité de cours), règles conditionnelles (si score faible → soutien) |

```
                    ┌─────────────────────┐
                    │   Données brutes     │
                    │ (Excel / CSV / SQL)  │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌───────────┐ ┌────────────┐ ┌───────────────┐
          │ Prédiction│ │Segmentation│ │Recommandation │
          │(Classif.) │ │(Clustering)│ │(Content/Règles)│
          └─────┬─────┘ └─────┬──────┘ └───────┬────────┘
                 ▼             ▼               ▼
          ┌─────────────────────────────────────────┐
          │   Dashboard & Recommandations actionnables│
          └─────────────────────────────────────────┘
```

---

## 👥 Répartition par binôme

### 🟦 Binôme 1 — Performance académique
| Tâche | Description |
|---|---|
| **Prédiction** | Prédire l'option choisie (Java, Python, Cloud, IA…) selon les notes précédentes et préférences |
| **Segmentation** | Regrouper les apprenants par résultats scolaires (faibles / moyens / excellents) |
| **Recommandation** | Recommander le prochain cours ou la spécialité la plus adaptée |

### 🟩 Binôme 2 — Niveaux et progression
| Tâche | Description |
|---|---|
| **Prédiction** | Prédire le niveau atteint (Level 1, 2, 3…) selon les cours suivis et les scores |
| **Segmentation** | Regrouper les apprenants selon leurs soft skills (communication, leadership, créativité) |
| **Recommandation** | Proposer un parcours de formation personnalisé (ex : renforcement en communication) |

### 🟨 Binôme 3 — Satisfaction et expérience
| Tâche | Description |
|---|---|
| **Prédiction** | Prédire le taux de satisfaction à partir des feedbacks et résultats |
| **Segmentation** | Regrouper les apprenants selon leur région/origine |
| **Recommandation** | Recommander des améliorations du centre (cours pratiques, organisation…) |

---

## 🗂 Dataset

Le dataset peut être **fictif ou réel**, structuré au format Excel/CSV, avec les colonnes suivantes :

<details>
<summary><strong>📁 Informations générales</strong></summary>

| Colonne | Description |
|---|---|
| `ID` | Identifiant unique de l'apprenant |
| `Âge` | Âge de l'apprenant |
| `Sexe` | Genre |
| `Région` | Zone géographique |

</details>

<details>
<summary><strong>📚 Données académiques</strong></summary>

| Colonne | Description |
|---|---|
| `Cours_suivis` | Java, Python, Cloud, IA, etc. |
| `Scores` | Note sur 100 |
| `Niveau` | Level 1/2/3 (ou Beginner/Intermediate/Advanced) |
| `Absences` | Nombre d'heures manquées |

</details>

<details>
<summary><strong>🤝 Soft skills</strong></summary>

| Colonne | Description |
|---|---|
| `Communication` | Score de 1 à 5 |
| `Travail_en_équipe` | Score de 1 à 5 |
| `Créativité` | Score de 1 à 5 |

</details>

<details>
<summary><strong>⭐ Satisfaction</strong></summary>

| Colonne | Description |
|---|---|
| `Avis` | Note globale (1 à 5) |
| `Commentaires` | Texte libre (optionnel, exploitable en NLP) |

</details>

> 💡 Le champ `Commentaires` peut être exploité ultérieurement via une analyse de sentiment (NLP) pour enrichir la prédiction de satisfaction.

---

## 🧰 Stack technique

| Catégorie | Outils |
|---|---|
| **Langage** | Python 3.10+ |
| **Manipulation de données** | Pandas, NumPy |
| **Visualisation** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Clustering / réduction de dimension** | K-Means, DBSCAN, PCA (scikit-learn) |
| **Environnement** | Jupyter Notebook / JupyterLab |
| **Suivi d'expériences** *(optionnel)* | MLflow |
| **Présentation** | Notebook final + slides (PowerPoint / Google Slides) |

---

## 🔬 Méthodologie CRISP-DM

Le projet suit rigoureusement le standard **CRISP-DM** (Cross Industry Standard Process for Data Mining) :

1. **🎯 Compréhension métier** — améliorer la formation et la satisfaction des apprenants
2. **🔍 Compréhension des données** — exploration des colonnes (scores, cours, avis, distributions, corrélations)
3. **🧹 Préparation des données** — nettoyage des valeurs manquantes/aberrantes, encodage des variables catégorielles, normalisation/standardisation
4. **🤖 Modélisation** — application des 9 objectifs (3 par binôme), entraînement et validation croisée
5. **📊 Évaluation** — Accuracy, F1-score, RMSE, Silhouette score selon la tâche
6. **🎤 Présentation finale** — notebook documenté + slides (résultats, graphiques, recommandations)

---

## 📁 Structure du projet

```
centre-formation-intelligent/
│
├── data/
│   ├── raw/                     # Données brutes (CSV/Excel)
│   ├── processed/                # Données nettoyées et encodées
│   └── dictionary.md             # Dictionnaire de données
│
├── notebooks/
│   ├── 01_exploration.ipynb      # Analyse exploratoire (EDA)
│   ├── 02_preprocessing.ipynb    # Nettoyage & feature engineering
│   ├── binome1_performance/
│   │   ├── prediction_option.ipynb
│   │   ├── segmentation_resultats.ipynb
│   │   └── recommandation_cours.ipynb
│   ├── binome2_progression/
│   │   ├── prediction_niveau.ipynb
│   │   ├── segmentation_softskills.ipynb
│   │   └── recommandation_parcours.ipynb
│   └── binome3_satisfaction/
│       ├── prediction_satisfaction.ipynb
│       ├── segmentation_region.ipynb
│       └── recommandation_ameliorations.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── models.py
│   ├── clustering.py
│   ├── recommender.py
│   └── evaluation.py
│
├── reports/
│   ├── figures/                  # Graphiques exportés
│   └── slides/                   # Présentation finale
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
# 1. Cloner le repository
git clone https://github.com/votre-org/centre-formation-intelligent.git
cd centre-formation-intelligent

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer Jupyter
jupyter notebook
```

**`requirements.txt` recommandé :**
```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
xgboost>=2.0
matplotlib>=3.7
seaborn>=0.12
plotly>=5.15
jupyter>=1.0
```

---

## 🔄 Pipeline d'exécution

| Étape | Notebook / Script | Sortie |
|---|---|---|
| 1️⃣ Exploration | `01_exploration.ipynb` | Statistiques descriptives, distributions, corrélations |
| 2️⃣ Préparation | `02_preprocessing.ipynb` | Dataset nettoyé et encodé (`data/processed/`) |
| 3️⃣ Prédiction | `prediction_*.ipynb` (×3) | Modèles entraînés + rapport de classification |
| 4️⃣ Segmentation | `segmentation_*.ipynb` (×3) | Clusters + visualisation ACP |
| 5️⃣ Recommandation | `recommandation_*.ipynb` (×3) | Règles/recommandations personnalisées |
| 6️⃣ Synthèse | `reports/slides/` | Présentation finale des résultats |

---

## 📐 Métriques d'évaluation

| Tâche | Métriques utilisées |
|---|---|
| **Classification** (prédiction) | Accuracy, Precision, Recall, F1-score, Matrice de confusion, ROC-AUC |
| **Régression** (si satisfaction en continu) | RMSE, MAE, R² |
| **Clustering** (segmentation) | Silhouette score, Inertie (méthode du coude), Davies-Bouldin index |
| **Recommandation** | Taux de pertinence perçue, Précision@k (si évaluation possible) |

---

## 💡 Exemple concret

> **Cas :** un apprenant a de bonnes notes en Python mais de mauvaises notes en Java.

| Axe | Résultat |
|---|---|
| 🔮 Prédiction | Option la plus probable → **Python avancé** |
| 🧩 Segmentation | Groupe **"bons en programmation, faibles en algorithmique"** |
| 🎯 Recommandation | Suivre un **atelier d'algorithmique** ciblé |

---

## 📦 Livrables

- ✅ Notebook Jupyter complet et commenté (9 objectifs)
- ✅ Dataset nettoyé et documenté
- ✅ Modèles entraînés et évalués (métriques à l'appui)
- ✅ Visualisations (distributions, clusters, importance des features)
- ✅ Slides de présentation finale avec recommandations concrètes pour le centre

---

## 🗺 Roadmap

- [ ] Finaliser l'exploration et le nettoyage des données
- [ ] Implémenter les 3 modèles de prédiction (un par binôme)
- [ ] Implémenter les 3 modules de segmentation
- [ ] Implémenter les 3 moteurs de recommandation
- [ ] Comparer les modèles (baseline vs XGBoost/Random Forest)
- [ ] Rédiger le rapport final et les slides
- [ ] *(Bonus)* Déployer un dashboard interactif (Streamlit/Dash)
- [ ] *(Bonus)* Analyse de sentiment sur les `Commentaires` (NLP)

---

## 📫 Contact

**Sujet du projet :** *Prédiction et amélioration des parcours d'apprenants dans un centre de formation à l'aide du Machine Learning*

Pour toute question relative au projet, contactez l'équipe pédagogique ou les binômes responsables de chaque axe.
