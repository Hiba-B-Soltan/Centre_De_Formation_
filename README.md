# 🎓 Smart Training Center
### Predict. Segment. Recommend. — ML for Learner Success

A Machine Learning project that turns raw learner data (academic, behavioral, satisfaction) into **actionable decisions** — predicting success, clustering learner profiles, and recommending personalized paths.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Classification-EA4C89)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![CRISP--DM](https://img.shields.io/badge/Methodology-CRISP--DM-blueviolet)
![Status](https://img.shields.io/badge/status-academic%20project-lightgrey)

---

## 🚀 Overview

> "From reactive management to **predictive, personalized** training."

Training centers sit on a goldmine of unused data — grades, courses, soft skills, feedback. This project mines it with **3 ML pillars**:

🔮 **Predict** learner outcomes &nbsp;|&nbsp; 🧩 **Segment** learner profiles &nbsp;|&nbsp; 🎯 **Recommend** personalized actions

---

## 🧠 The 3 ML Pillars

| Pillar | Problem Type | Algorithms |
|---|---|---|
| 🔮 **Prediction** | Classification | Logistic Regression, Random Forest, SVM, XGBoost |
| 🧩 **Segmentation** | Clustering | K-Means, DBSCAN, PCA |
| 🎯 **Recommendation** | Content-based / Rules | Course similarity, if-then business rules |

```
   Raw Data (CSV/Excel)
          │
   ┌──────┼──────┐
   ▼      ▼      ▼
Predict Segment Recommend
   └──────┼──────┘
          ▼
  Actionable Insights 📊
```

---

## 👥 Team Split — 9 Objectives, 3 Duos

<table>
<tr><th>Duo</th><th>🔮 Prediction</th><th>🧩 Segmentation</th><th>🎯 Recommendation</th></tr>
<tr>
<td><b>1️⃣ Academic Performance</b></td>
<td>Predict chosen track (Java/Python/Cloud)</td>
<td>Cluster by academic results</td>
<td>Suggest next best course</td>
</tr>
<tr>
<td><b>2️⃣ Level & Progression</b></td>
<td>Predict level reached (1/2/3)</td>
<td>Cluster by soft skills</td>
<td>Personalized learning path</td>
</tr>
<tr>
<td><b>3️⃣ Satisfaction & Experience</b></td>
<td>Predict satisfaction score</td>
<td>Cluster by region</td>
<td>Suggest center improvements</td>
</tr>
</table>

---

## 🗂 Dataset

| Category | Columns |
|---|---|
| 👤 **Profile** | `ID`, `Age`, `Gender`, `Region` |
| 📚 **Academics** | `Courses`, `Scores`, `Level`, `Absences` |
| 🤝 **Soft Skills** | `Communication`, `Teamwork`, `Creativity` (1–5) |
| ⭐ **Satisfaction** | `Rating` (1–5), `Comments` (free text) |

> 💡 `Comments` can later power an NLP sentiment layer for richer satisfaction prediction.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| Viz | Matplotlib, Seaborn, Plotly |
| ML | Scikit-learn, XGBoost |
| Environment | Jupyter Notebook |

---

## 🔬 Methodology — CRISP-DM

`Business Understanding` → `Data Understanding` → `Data Prep` → `Modeling (9 objectives)` → `Evaluation` → `Final Presentation`

---

## ⚙️ Quick Start

```bash
git clone https://github.com/your-org/smart-training-center.git
cd smart-training-center
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

---

## 📐 Evaluation Metrics

| Task | Metrics |
|---|---|
| Classification | Accuracy, F1-score, ROC-AUC |
| Clustering | Silhouette score, Elbow method |
| Regression | RMSE, MAE |

---

## 💡 Example in Action

> A learner scores high in **Python**, low in **Java**.

🔮 Prediction → *Advanced Python track* &nbsp;|&nbsp; 🧩 Segment → *"Strong coder, weak in algorithms"* &nbsp;|&nbsp; 🎯 Recommendation → *Algorithm workshop*

---

## 📦 Deliverables

✅ Full annotated notebook (9 objectives) &nbsp; ✅ Clean dataset &nbsp; ✅ Trained & evaluated models &nbsp; ✅ Visualizations &nbsp; ✅ Final slides with recommendations

---

## 🗺 Roadmap

- [ ] EDA & data cleaning
- [ ] Build 3 prediction models
- [ ] Build 3 segmentation modules
- [ ] Build 3 recommendation engines
- [ ] Compare models & finalize report
- [ ] 🎁 *Bonus:* Interactive dashboard (Streamlit)
- [ ] 🎁 *Bonus:* NLP sentiment on comments

---

## 📫 Contact Hiba Ben Soltan hiba.bensoltan@esprit.tn

**Project theme:** *Predicting and enhancing learner journeys in a training center using Machine Learning*
