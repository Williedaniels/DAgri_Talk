import React, { useState, useEffect } from 'react';
import { marketAPI } from '../services/api';
import { MarketListing } from '../types';

const Market: React.FC = () => {
  const [listings, setListings] = useState<MarketListing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await marketAPI.getAll();
        setListings(response.data);
      } catch (error) {
        console.error('Failed to fetch market listings:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, []);

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading market listings...</div>;
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ color: '#2e7d32', marginBottom: '2rem' }}>Farmer Marketplace</h1>
      
      {listings.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <p>No market listings yet. Farmers can start listing their produce here!</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          {listings.map((listing) => (
            <div key={listing.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1.5rem' }}>
              <h3 style={{ color: '#2e7d32', marginBottom: '0.5rem' }}>{listing.crop_name}</h3>
              <div style={{ marginBottom: '1rem' }}>
                <p><strong>Quantity:</strong> {listing.quantity} {listing.unit}</p>
                <p><strong>Price:</strong> ${listing.price_per_unit} per {listing.unit}</p>
                <p><strong>Location:</strong> {listing.location}</p>
                <p><strong>Farmer:</strong> {listing.farmer}</p>
              </div>
              {listing.description && (
                <p style={{ color: '#666', marginBottom: '1rem' }}>{listing.description}</p>
              )}
              <div style={{ fontSize: '0.8rem', color: '#999' }}>
                Listed: {new Date(listing.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Market;