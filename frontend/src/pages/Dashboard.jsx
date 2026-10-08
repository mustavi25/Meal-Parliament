import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { username, logout } = useAuth();
  const navigate = useNavigate();
  const [households, setHouseholds] = useState([]);
  const [name, setName] = useState('');
  const [customCode, setCustomCode] = useState('');
  const [code, setCode] = useState('');
  const [message, setMessage] = useState('');

  const loadHouseholds = async () => {
    const res = await api.get('/households/');
    setHouseholds(res.data);
  };

  useEffect(() => { loadHouseholds(); }, []);

  const createHousehold = async (e) => {
    e.preventDefault();
    try {
      await api.post('/households/', { name, invite_code: customCode });
      setName('');
      setCustomCode('');
      setMessage('Household created!');
      loadHouseholds();
    } catch (err) {
      const data = err.response?.data;
      setMessage(data?.invite_code?.[0] || data?.name?.[0] || 'Could not create household.');
    }
  };

  const joinHousehold = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/households/join/', { invite_code: code });
      setMessage(res.data.message);
      setCode('');
      loadHouseholds();
    } catch (err) {
      setMessage(err.response?.data?.error || 'Could not join household.');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <h2>Welcome, {username}!</h2>
      <button onClick={handleLogout}>Logout</button>
      {message && <p>{message}</p>}

      <h3>Your Households</h3>
      {households.length === 0 ? (
        <p>You're not in any households yet.</p>
      ) : (
        <ul>
          {households.map((h) => (
            <li key={h.id}>{h.name} (invite code: {h.invite_code})</li>
          ))}
        </ul>
      )}

      <h3>Create a household</h3>
      <form onSubmit={createHousehold}>
        <input placeholder="Household name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Invite code (optional)" value={customCode} onChange={(e) => setCustomCode(e.target.value)} />
        <button type="submit">Create</button>
      </form>

      <h3>Join with invite code</h3>
      <form onSubmit={joinHousehold}>
        <input placeholder="Invite code" value={code} onChange={(e) => setCode(e.target.value)} />
        <button type="submit">Join</button>
      </form>
    </div>
  );
}