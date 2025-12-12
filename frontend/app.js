document.getElementById("student-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;

    document.getElementById("loading").classList.remove("d-none");
    document.getElementById("result-area").classList.add("d-none");
    document.getElementById("error").classList.add("d-none");

    const payload = {
        age: form.age.value,
        gender: form.gender.value,
        region: form.region.value,
        math_score: Number(form.math_score.value),
        physics_score: Number(form.physics_score.value),
        literature_score: Number(form.literature_score.value),
        english_score: Number(form.english_score.value),
        communication: Number(form.communication.value),
        teamwork: Number(form.teamwork.value),
        leadership: Number(form.leadership.value),
        problem_solving: Number(form.problem_solving.value),
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
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

        document.getElementById("pred-level").textContent = result.predicted_level;
        document.getElementById("pred-cluster").textContent = "Cluster " + result.cluster_soft;
        document.getElementById("pred-reco").innerHTML = result.recommendation;

        document.getElementById("loading").classList.add("d-none");
        document.getElementById("result-area").classList.remove("d-none");

        // 🔥 AFFICHER LA COLONNE DES RÉSULTATS APRÈS ANALYSE
        document.getElementById("results-column").classList.remove("d-none");

    } catch (err) {
        console.error(err);
        document.getElementById("loading").classList.add("d-none");
        document.getElementById("error").textContent = "Erreur de connexion avec le serveur.";
        document.getElementById("error").classList.remove("d-none");
    }
});
