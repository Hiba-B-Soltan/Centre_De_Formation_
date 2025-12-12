async function fetchStudents() {
  const select = document.getElementById("student-select");
  if (!select) return;
  try {
    const res = await fetch("http://127.0.0.1:8000/students");
    const data = await res.json();
    (Array.isArray(data) ? data : []).forEach((s) => {
      const opt = document.createElement("option");
      opt.value = String(s.student_id || "");
      opt.textContent = `${s.student_name || `Étudiant ${s.student_id}`}`;
      select.appendChild(opt);
    });

    select.addEventListener("change", () => {
      const id = select.value;
      const st = (Array.isArray(data) ? data : []).find((x) => String(x.student_id) === id);
      if (!st) return;
      const form = document.getElementById("student-form");
      form.math_score.value = st.math_score ?? 0;
      form.physics_score.value = st.physics_score ?? 0;
      form.literature_score.value = st.literature_score ?? 0;
      form.english_score.value = st.english_score ?? 0;
      form.communication.value = st.communication ?? 0;
      form.teamwork.value = st.teamwork ?? 0;
      form.leadership.value = st.leadership ?? 0;
      form.problem_solving.value = st.problem_solving ?? 0;
      form.age.value = st.age ?? 0;
      form.parent_income.value = st.parent_income ?? 0;
      form.attendance_rate.value = st.attendance_rate ?? 0;
    });
  } catch (_) {}
}

document.addEventListener("DOMContentLoaded", fetchStudents);

document.getElementById("student-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;

  document.getElementById("loading").classList.remove("d-none");
  document.getElementById("result-area").classList.add("d-none");
  document.getElementById("error").classList.add("d-none");

  const payload = {
    math_score: Number(form.math_score.value),
    physics_score: Number(form.physics_score.value),
    literature_score: Number(form.literature_score.value),
    english_score: Number(form.english_score.value),
    communication: Number(form.communication.value),
    teamwork: Number(form.teamwork.value),
    leadership: Number(form.leadership.value),
    problem_solving: Number(form.problem_solving.value),
    age: Number(form.age.value),
    parent_income: Number(form.parent_income.value),
    attendance_rate: Number(form.attendance_rate.value),
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (result.error) {
      document.getElementById("error").textContent = result.error;
      document.getElementById("error").classList.remove("d-none");
      document.getElementById("loading").classList.add("d-none");
      return;
    }

    document.getElementById("rec-option").textContent = result.recommended_option;
    document.getElementById("rec-cluster").textContent = String(result.cluster).toUpperCase();

    const courses = document.getElementById("rec-courses");
    courses.innerHTML = "";
    (result.recommended_courses || []).forEach((c) => {
      const li = document.createElement("li");
      li.textContent = c;
      courses.appendChild(li);
    });

    const probs = document.getElementById("rec-probabilities");
    probs.innerHTML = "";
    const probsObj = result.option_probabilities || {};
    Object.keys(probsObj).forEach((opt) => {
      const percent = Number(probsObj[opt]) || 0;
      const wrap = document.createElement("div");
      wrap.className = "mb-2";
      const header = document.createElement("div");
      header.className = "d-flex justify-content-between mb-1";
      header.innerHTML = `<span class="fw-medium">${opt}</span><span class="text-muted">${percent}%</span>`;
      const barWrap = document.createElement("div");
      barWrap.className = "w-100 bg-secondary bg-opacity-25 rounded";
      const bar = document.createElement("div");
      bar.className = "bg-primary rounded";
      bar.style.height = "8px";
      bar.style.width = `${percent}%`;
      barWrap.appendChild(bar);
      wrap.appendChild(header);
      wrap.appendChild(barWrap);
      probs.appendChild(wrap);
    });

    const expl = document.getElementById("rec-explanations");
    expl.innerHTML = "";
    const top = (result.explanations && result.explanations.top_features) || [];
    top.forEach((f) => {
      const row = document.createElement("div");
      row.className = "d-flex justify-content-between mb-1";
      row.innerHTML = `<div class="fw-medium">${String(f.name).replace('_', ' ')}</div>
        <div class="text-muted">Imp: ${f.importance}% · Vous: ${f.student_value} · Moy: ${f.dataset_mean}</div>`;
      expl.appendChild(row);
    });

    const tbl = document.getElementById("rec-similar");
    tbl.innerHTML = "";
    (result.similar_students || []).forEach((s) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${s.student_id}</td><td>${s.preferred_option || ''}</td>`;
      tbl.appendChild(tr);
    });

    document.getElementById("loading").classList.add("d-none");
    document.getElementById("result-area").classList.remove("d-none");
  } catch (err) {
    document.getElementById("loading").classList.add("d-none");
    document.getElementById("error").textContent = "Erreur de connexion avec le serveur.";
    document.getElementById("error").classList.remove("d-none");
  }
});
