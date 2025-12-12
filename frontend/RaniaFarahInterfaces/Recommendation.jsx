// src/pages/Recommendation.jsx
import React, { useState } from 'react';
import api from '../config/api';

const Recommendation = () => {
  const [formData, setFormData] = useState({
    math_score: '',
    physics_score: '',
    literature_score: '',
    english_score: '',
    communication: '',
    teamwork: '',
    leadership: '',
    problem_solving: '',
    age: '',
    parent_income: '',
    attendance_rate: ''
  });
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [students, setStudents] = useState([]);
  const [selectedStudentId, setSelectedStudentId] = useState('');

  React.useEffect(() => {
    const fetchStudents = async () => {
      try {
        const res = await fetch(`${api.BASE_URL}${api.ENDPOINTS.STUDENTS}`);
        if (res.ok) {
          const data = await res.json();
          setStudents(Array.isArray(data) ? data : []);
        }
      } catch (_) {}
    };
    fetchStudents();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${api.BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des recommandations');
      }

      const data = await response.json();
      setRecommendation(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section max-w-4xl">
      <h1 className="heading mb-6">Recommandation de Formation</h1>
      <div className="panel mb-6">
        <label className="block text-gray-700 text-sm font-bold mb-2">Sélectionner un étudiant existant</label>
        <select
          className="input"
          value={selectedStudentId}
          onChange={(e) => {
            const id = e.target.value;
            setSelectedStudentId(id);
            const st = students.find(s => String(s.student_id) === id);
            if (st) {
              const updated = {
                math_score: st.math_score ?? 0,
                physics_score: st.physics_score ?? 0,
                literature_score: st.literature_score ?? 0,
                english_score: st.english_score ?? 0,
                communication: st.communication ?? 0,
                teamwork: st.teamwork ?? 0,
                leadership: st.leadership ?? 0,
                problem_solving: st.problem_solving ?? 0,
                age: st.age ?? 0,
                parent_income: st.parent_income ?? 0,
                attendance_rate: st.attendance_rate ?? 0
              };
              setFormData(updated);
            }
          }}
        >
          <option value="">-- Choisir --</option>
          {students.map(s => (
            <option key={s.student_id} value={String(s.student_id)}>
              {s.student_name} ({s.student_id})
            </option>
          ))}
        </select>
      </div>
      
      <form onSubmit={handleSubmit} className="panel mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(formData).map(([key, value]) => (
            <div key={key} className="mb-4">
              <label className="label capitalize mb-2">
                {key.replace('_', ' ')}
              </label>
              <input
                type="number"
                name={key}
                value={value}
                onChange={handleChange}
                className="input"
                min="0"
                max={key.includes('score') ? 20 : key === 'attendance_rate' ? 1 : 100}
                step={key === 'attendance_rate' ? 0.01 : 0.1}
                required
              />
            </div>
          ))}
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="btn-primary disabled:opacity-50"
        >
          {loading ? 'Chargement...' : 'Obtenir une recommandation'}
        </button>
      </form>

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p className="font-bold">Erreur</p>
          <p>{error}</p>
        </div>
      )}

      {recommendation && (
        <div className="space-y-6">
          <div className="panel bg-green-50">
            <h2 className="text-xl font-bold mb-2">Option recommandée :</h2>
            <p className="text-2xl font-bold">{recommendation.recommended_option}</p>
            <p className="mt-2">Confiance : {recommendation.option_probabilities[recommendation.recommended_option]}%</p>
          </div>

          <div className="panel bg-blue-50">
            <h3 className="text-xl font-semibold mb-2">Cluster du profil</h3>
            <p className="text-lg">{String(recommendation.cluster).toUpperCase()}</p>
          </div>

          <div className="panel">
            <h3 className="text-xl font-semibold mb-4">Parcours suggéré :</h3>
            <ul className="list-disc pl-6 space-y-2">
              {recommendation.recommended_courses.map((course, index) => (
                <li key={index} className="text-gray-700">{course}</li>
              ))}
            </ul>
          </div>

          <div className="panel">
            <h3 className="text-xl font-semibold mb-4">Probabilités par option :</h3>
            <div className="space-y-2">
              {Object.entries(recommendation.option_probabilities).map(([option, prob]) => (
                <div key={option} className="mb-2">
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">{option}</span>
                    <span className="text-gray-600">{prob}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div 
                      className="bg-blue-600 h-2.5 rounded-full" 
                      style={{ width: `${prob}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {recommendation.explanations && recommendation.explanations.top_features && (
            <div className="panel">
              <h3 className="text-xl font-semibold mb-4">Justification du modèle :</h3>
              <div className="space-y-3">
                {recommendation.explanations.top_features.map((f, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="font-medium capitalize">{f.name.replace('_', ' ')}</div>
                      <div className="text-xs text-gray-600">Importance: {f.importance}%</div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-sm text-gray-700">Vous: {f.student_value}</div>
                      <div className="text-sm text-gray-500">Moyenne: {f.dataset_mean}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="panel">
            <h3 className="text-xl font-semibold mb-4">Étudiants ayant un profil similaire :</h3>
            <div className="overflow-x-auto">
              <table className="table">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID Étudiant
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Option choisie
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recommendation.similar_students.map((student, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {student.student_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {student.preferred_option}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Recommendation;
