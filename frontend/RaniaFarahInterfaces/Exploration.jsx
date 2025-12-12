import React, { useState, useEffect } from 'react';
import api from '../config/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Exploration = () => {
  const [overview, setOverview] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCluster, setSelectedCluster] = useState('');
  const [selectedOption, setSelectedOption] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ovRes, stRes] = await Promise.all([
          fetch(`${api.BASE_URL}${api.ENDPOINTS.EXPLORE}`),
          fetch(`${api.BASE_URL}${api.ENDPOINTS.STUDENTS_CLUSTERS}`)
        ]);
        if (!ovRes.ok || !stRes.ok) {
          throw new Error('Erreur lors du chargement des données');
        }
        const ov = await ovRes.json();
        const st = await stRes.json();
        setOverview(ov);
        setStudents(Array.isArray(st) ? st : []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="section">Chargement des données...</div>;
  if (error) return <div className="section text-red-600">Erreur: {error}</div>;

  return (
    <div className="section">
      <h1 className="heading mb-6">Explorer les Formations</h1>
      {overview && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="panel">
            <h2 className="text-xl font-semibold mb-4">Comptes par spécialité</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={overview.option_counts}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="preferred_option" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#4f46e5" name="Nombre" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="panel">
            <h2 className="text-xl font-semibold mb-4">Comptes par cluster</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={overview.cluster_counts}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="cluster" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#10b981" name="Nombre" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="panel">
            <h2 className="text-xl font-semibold mb-4">Moyennes par cluster</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={overview.avg_scores_by_cluster}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="cluster" />
                  <YAxis domain={[0, 20]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="math_score" fill="#4f46e5" name="Maths" />
                  <Bar dataKey="physics_score" fill="#10b981" name="Physique" />
                  <Bar dataKey="literature_score" fill="#f59e0b" name="Littérature" />
                  <Bar dataKey="english_score" fill="#ef4444" name="Anglais" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      <div className="panel mb-6">
        <h2 className="text-xl font-semibold mb-4">Filtres</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Cluster</label>
            <select className="input" value={selectedCluster} onChange={(e) => setSelectedCluster(e.target.value)}>
              <option value="">Tous</option>
              <option value="faible">Faible</option>
              <option value="moyen">Moyen</option>
              <option value="excellent">Excellent</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Spécialité</label>
            <select className="input" value={selectedOption} onChange={(e) => setSelectedOption(e.target.value)}>
              <option value="">Toutes</option>
              {(overview?.formations || []).map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="panel">
        <h2 className="text-xl font-semibold mb-4">Profils d’apprenants</h2>
        <div className="overflow-x-auto">
          <table className="table">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Spécialité</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cluster</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Maths</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Physique</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Littérature</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Anglais</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {students
                .filter(s => (selectedCluster ? s.cluster === selectedCluster : true))
                .filter(s => (selectedOption ? s.preferred_option === selectedOption : true))
                .slice(0, 200)
                .map((s) => (
                  <tr key={s.student_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{s.student_id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.preferred_option}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.cluster}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.math_score}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.physics_score}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.literature_score}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.english_score}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Exploration;
