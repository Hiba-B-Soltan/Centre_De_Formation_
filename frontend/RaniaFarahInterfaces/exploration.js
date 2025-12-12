async function loadData() {
  try {
    const [overviewRes, clustersRes] = await Promise.all([
      fetch("http://127.0.0.1:8000/explore"),
      fetch("http://127.0.0.1:8000/students_clusters")
    ]);
    if (!overviewRes.ok || !clustersRes.ok) throw new Error("Erreur lors du chargement des données");

    const overview = await overviewRes.json();
    const clustersData = await clustersRes.json();

    const optionCounts = Array.isArray(overview.option_counts) ? overview.option_counts : [];
    const clusterCounts = Array.isArray(overview.cluster_counts) ? overview.cluster_counts : [];
    const avgScoresByCluster = Array.isArray(overview.avg_scores_by_cluster) ? overview.avg_scores_by_cluster : [];

    const optionLabels = optionCounts.map((o) => String(o.preferred_option || 'Inconnu'));
    const optionValues = optionCounts.map((o) => Number(o.count || 0));
    const clusterLabels = clusterCounts.map((c) => String(c.cluster || 'Inconnu'));
    const clusterValues = clusterCounts.map((c) => Number(c.count || 0));

    const scoreNames = ["math_score", "physics_score", "literature_score", "english_score"];
    const avgLabels = avgScoresByCluster.map((r) => String(r.cluster || 'Inconnu'));
    const datasets = scoreNames
      .filter((s) => avgScoresByCluster.some((r) => typeof r[s] !== 'undefined'))
      .map((s, i) => ({
        label: s.replace('_score', '').replace('_', ' '),
        data: avgScoresByCluster.map((r) => Number(r[s] || 0)),
        backgroundColor: [
          'rgba(99, 102, 241, 0.45)',  // Indigo
          'rgba(16, 185, 129, 0.45)',  // Emerald
          'rgba(251, 191, 36, 0.45)',  // Amber
          'rgba(248, 113, 113, 0.45)'  // Red
        ][i % 4]
      }));

    const ctxOptions = document.getElementById('chartOptions').getContext('2d');
    new Chart(ctxOptions, {
      type: 'bar',
      data: { labels: optionLabels, datasets: [{ label: 'Comptes', data: optionValues, backgroundColor: 'rgba(99, 102, 241, 0.35)' }] },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(0,0,0,0.06)' } }, x: { grid: { color: 'rgba(0,0,0,0.06)' } } } }
    });

    const ctxClusters = document.getElementById('chartClusters').getContext('2d');
    new Chart(ctxClusters, {
      type: 'bar',
      data: { labels: clusterLabels, datasets: [{ label: 'Comptes', data: clusterValues, backgroundColor: 'rgba(16, 185, 129, 0.35)' }] },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(0,0,0,0.06)' } }, x: { grid: { color: 'rgba(0,0,0,0.06)' } } } }
    });

    const ctxAvg = document.getElementById('chartAvgScores').getContext('2d');
    new Chart(ctxAvg, {
      type: 'bar',
      data: { labels: avgLabels, datasets },
      options: { responsive: true, scales: { y: { grid: { color: 'rgba(0,0,0,0.06)' } }, x: { grid: { color: 'rgba(0,0,0,0.06)' } } } }
    });

    const optionSelect = document.getElementById('filterOption');
    optionSelect.innerHTML = '<option value="">Toutes</option>';
    (Array.isArray(overview.formations) ? overview.formations : []).forEach((opt) => {
      const o = document.createElement('option');
      o.value = String(opt);
      o.textContent = String(opt);
      optionSelect.appendChild(o);
    });

    const students = Array.isArray(clustersData.students) ? clustersData.students : [];
    const tableBody = document.getElementById('studentsTable');
    const filterCluster = document.getElementById('filterCluster');

    function renderTable() {
      const fc = filterCluster.value;
      const fo = optionSelect.value;
      const rows = students.filter((s) => {
        const okCluster = fc ? String(s.cluster) === fc : true;
        const okOption = fo ? String(s.preferred_option) === fo : true;
        return okCluster && okOption;
      });
      tableBody.innerHTML = '';
      rows.forEach((s) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${s.student_id ?? ''}</td>
          <td>${s.preferred_option ?? ''}</td>
          <td>${s.cluster ?? ''}</td>
          <td>${s.math_score ?? ''}</td>
          <td>${s.physics_score ?? ''}</td>
          <td>${s.literature_score ?? ''}</td>
          <td>${s.english_score ?? ''}</td>
        `;
        tableBody.appendChild(tr);
      });
    }

    filterCluster.addEventListener('change', renderTable);
    optionSelect.addEventListener('change', renderTable);
    renderTable();
  } catch (err) {
    console.error(err);
    alert('Erreur de connexion avec le serveur. Vérifiez que l’API Flask tourne sur http://127.0.0.1:8000.');
  }
}

document.addEventListener('DOMContentLoaded', loadData);
