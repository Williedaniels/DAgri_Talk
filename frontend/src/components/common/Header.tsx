import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <header style={{ padding: '1rem', backgroundColor: '#2e7d32', color: 'white' }}>
      <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>
          D'Agri Talk
        </Link>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/knowledge" style={{ color: 'white', textDecoration: 'none' }}>Knowledge</Link>
          <Link to="/market" style={{ color: 'white', textDecoration: 'none' }}>Market</Link>
          {token ? (
            <button onClick={handleLogout} style={{ background: 'none', border: '1px solid white', color: 'white', padding: '0.5rem 1rem', cursor: 'pointer' }}>
              Logout
            </button>
          ) : (
            <>
              <Link to="/login" style={{ color: 'white', textDecoration: 'none' }}>Login</Link>
              <Link to="/register" style={{ color: 'white', textDecoration: 'none' }}>Register</Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;