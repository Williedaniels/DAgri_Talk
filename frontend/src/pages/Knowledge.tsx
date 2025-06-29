import React, { useState, useEffect } from 'react';
import { knowledgeAPI } from '../services/api';
import { KnowledgeEntry } from '../types';

const Knowledge: React.FC = () => {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const response = await knowledgeAPI.getAll();
        setEntries(response.data);
      } catch (error) {
        console.error('Failed to fetch knowledge entries:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEntries();
  }, []);

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading knowledge entries...</div>;
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ color: '#2e7d32', marginBottom: '2rem' }}>Traditional Agricultural Knowledge</h1>
      
      {entries.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>No knowledge entries yet. Be the first to share traditional farming wisdom!</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1.5rem' }}>
          {entries.map((entry) => (
            <div key={entry.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1.5rem' }}>
              <h3 style={{ color: '#2e7d32', marginBottom: '0.5rem' }}>{entry.title}</h3>
              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
                <span>By: {entry.author}</span>
                <span>Crop: {entry.crop_type}</span>
                <span>Region: {entry.region}</span>
                <span>Language: {entry.language}</span>
              </div>
              <p style={{ lineHeight: '1.6' }}>{entry.content}</p>
              <div style={{ fontSize: '0.8rem', color: '#999', marginTop: '1rem' }}>
                Created: {new Date(entry.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Knowledge;