import React from 'react';

const Home: React.FC = () => {
  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', color: '#2e7d32', marginBottom: '1rem' }}>
          Welcome to D'Agri Talk
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '0.5rem' }}>
          Traditional Agricultural Knowledge Platform for Liberia
        </p>
        <p style={{ fontSize: '1rem', color: '#666' }}>
          Connecting farmers, preserving wisdom, building communities
        </p>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '3rem' }}>
        <div style={{ padding: '2rem', border: '1px solid #ddd', borderRadius: '8px', textAlign: 'center' }}>
          <h3 style={{ color: '#2e7d32', marginBottom: '1rem' }}>Traditional Knowledge</h3>
          <p>Preserve and share ancestral farming wisdom from Liberian elders and experienced farmers.</p>
        </div>
        <div style={{ padding: '2rem', border: '1px solid #ddd', borderRadius: '8px', textAlign: 'center' }}>
          <h3 style={{ color: '#2e7d32', marginBottom: '1rem' }}>Market Connection</h3>
          <p>Connect farmers directly with buyers and access real-time market prices for your crops.</p>
        </div>
        <div style={{ padding: '2rem', border: '1px solid #ddd', borderRadius: '8px', textAlign: 'center' }}>
          <h3 style={{ color: '#2e7d32', marginBottom: '1rem' }}>Community Support</h3>
          <p>Learn from fellow farmers and experts through our community forums and discussions.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;