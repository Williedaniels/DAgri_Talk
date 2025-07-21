import React, { useState, useEffect } from 'react';
import { marketAPI } from '../services/api';
import { MarketListing } from '../types';
import { Button, Card, Alert, Input } from '../components/ui';

const Market: React.FC = () => {
  const [listings, setListings] = useState<MarketListing[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('all');
  const [selectedLocation, setSelectedLocation] = useState('all');

  const [newListing, setNewListing] = useState({
    crop_name: '',
    quantity: '',
    unit: 'kg',
    price_per_unit: '',
    location: '',
    description: '',
  });

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchListings();
  }, []);

  const fetchListings = async () => {
    try {
      const response = await marketAPI.getAll();
      // If API returns empty data, use mock data for demonstration
      if (!response.data || response.data.length === 0) {
      const mockData = [
        {
          id: 1,
          crop_name: "Organic Brown Rice",
          quantity: 50,
          unit: "bags",
          price_per_unit: 25.00,
          location: "Bong County",
          farmer: "Joseph Kpan",
          description: "High-quality organic brown rice grown using traditional methods. No chemicals used. Perfect for healthy eating.",
          is_available: true,
          created_at: "2024-07-15T08:00:00Z"
        },
        {
          id: 2,
          crop_name: "Fresh Cassava",
          quantity: 100,
          unit: "kg",
          price_per_unit: 1.50,
          location: "Nimba County",
          farmer: "Sarah Togba",
          description: "Fresh cassava harvested this week. Sweet variety, perfect for fufu or cassava bread.",
          is_available: true,
          created_at: "2024-07-18T10:30:00Z"
        },
        {
          id: 3,
          crop_name: "Premium Palm Oil",
          quantity: 20,
          unit: "lbs",
          price_per_unit: 8.00,
          location: "Grand Bassa County",
          farmer: "John Pewee",
          description: "Pure red palm oil extracted using traditional methods. Rich in vitamins and perfect for cooking.",
          is_available: true,
          created_at: "2024-07-16T14:20:00Z"
        },
        {
          id: 4,
          crop_name: "Cocoa Beans",
          quantity: 15,
          unit: "bags",
          price_per_unit: 45.00,
          location: "Maryland County",
          farmer: "Mary Kollie",
          description: "Premium quality cocoa beans, properly dried and fermented. Ready for export or local processing.",
          is_available: true,
          created_at: "2024-07-19T09:15:00Z"
        },
        {
          id: 5,
          crop_name: "Mixed Vegetables",
          quantity: 30,
          unit: "bundles",
          price_per_unit: 3.50,
          location: "Montserrado County",
          farmer: "Moses Gaye",
          description: "Fresh mixed vegetables including cabbage, lettuce, tomatoes, and peppers. Harvested daily.",
          is_available: true,
          created_at: "2024-07-20T06:45:00Z"
        },
        {
          id: 6,
          crop_name: "Sweet Potatoes",
          quantity: 75,
          unit: "kg",
          price_per_unit: 2.00,
          location: "Lofa County",
          farmer: "Grace Williams",
          description: "Sweet and nutritious sweet potatoes. Great for roasting, boiling, or making chips.",
          is_available: true,
          created_at: "2024-07-17T12:30:00Z"
        },
        {
          id: 7,
          crop_name: "Plantains",
          quantity: 200,
          unit: "pieces",
          price_per_unit: 0.75,
          location: "Grand Gedeh County",
          farmer: "Thomas Cooper",
          description: "Green plantains perfect for frying or boiling. Fresh from the farm, various sizes available.",
          is_available: true,
          created_at: "2024-07-19T15:20:00Z"
        },
        {
          id: 8,
          crop_name: "Pepper",
          quantity: 10,
          unit: "kg",
          price_per_unit: 12.00,
          location: "Sinoe County",
          farmer: "Elizabeth Johnson",
          description: "Hot pepper variety grown locally. Perfect for traditional Liberian dishes and sauces.",
          is_available: true,
          created_at: "2024-07-18T11:10:00Z"
        }
      ];
      setListings(mockData);
      setError('Using sample market listings for demonstration');
      } else {
        setListings(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch market listings:', error);
      setError('Failed to load market listings');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateListing = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      setError('Please login to create a market listing');
      return;
    }

    setCreateLoading(true);
    setError('');

    try {
      await marketAPI.create({
        ...newListing,
        quantity: parseFloat(newListing.quantity),
        price_per_unit: parseFloat(newListing.price_per_unit),
      });
      setSuccess('Market listing created successfully!');
      setNewListing({
        crop_name: '',
        quantity: '',
        unit: 'kg',
        price_per_unit: '',
        location: '',
        description: '',
      });
      setShowCreateForm(false);
      fetchListings();
      setTimeout(() => setSuccess(''), 3000);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to create market listing');
    } finally {
      setCreateLoading(false);
    }
  };

  // Filter listings based on search and filters
  const filteredListings = listings.filter(listing => {
    const matchesSearch = listing.crop_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         listing.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (listing.description && listing.description.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCrop = selectedCrop === 'all' || listing.crop_name.toLowerCase().includes(selectedCrop.toLowerCase());
    const matchesLocation = selectedLocation === 'all' || listing.location.toLowerCase().includes(selectedLocation.toLowerCase());
    
    return matchesSearch && matchesCrop && matchesLocation;
  });

  const uniqueCrops = Array.from(new Set(listings.map(listing => listing.crop_name).filter(Boolean)));
  const uniqueLocations = Array.from(new Set(listings.map(listing => listing.location).filter(Boolean)));
  const units = ['kg', 'lbs', 'bags', 'bundles', 'pieces'];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container-custom">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading marketplace...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container-custom">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🛒 Agricultural Marketplace
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Connect directly with farmers and buyers. Find fresh produce at fair prices 
            or list your harvest to reach more customers.
          </p>
        </div>

        {/* Alerts */}
        {error && (
          <Alert type="error" className="mb-6" onClose={() => setError('')}>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert type="success" className="mb-6" onClose={() => setSuccess('')}>
            {success}
          </Alert>
        )}

        {/* Action Bar */}
        <div className="bg-white rounded-xl shadow-soft border border-gray-200 p-6 mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex flex-col sm:flex-row gap-4 flex-1">
              {/* Search */}
              <div className="flex-1">
                <Input
                  type="text"
                  placeholder="Search products, locations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  icon={
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  }
                />
              </div>

              {/* Filters */}
              <div className="flex gap-4">
                <select
                  value={selectedCrop}
                  onChange={(e) => setSelectedCrop(e.target.value)}
                  className="form-input w-auto"
                >
                  <option value="all">All Products</option>
                  {uniqueCrops.map(crop => (
                    <option key={crop} value={crop}>{crop}</option>
                  ))}
                </select>

                <select
                  value={selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  className="form-input w-auto"
                >
                  <option value="all">All Locations</option>
                  {uniqueLocations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Create Listing Button */}
            {token && (
              <Button
                variant="primary"
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="w-full sm:w-auto"
              >
                {showCreateForm ? 'Cancel' : '📦 List Product'}
              </Button>
            )}
            
            {!token && (
              <p className="text-sm text-gray-500 text-center">
                <a href="/login" className="text-primary-600 hover:text-primary-700">Login</a> to list products
              </p>
            )}
          </div>
        </div>

        {/* Create Listing Form */}
        {showCreateForm && token && (
          <Card className="mb-8 animate-fade-in">
            <Card.Header>
              <h3 className="text-lg font-semibold text-gray-900">List Your Product</h3>
              <p className="text-sm text-gray-600">Share your harvest with the community and reach more buyers</p>
            </Card.Header>
            <Card.Body>
              <form onSubmit={handleCreateListing} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <Input
                    type="text"
                    label="Product Name"
                    placeholder="e.g., Organic Rice, Fresh Cassava"
                    value={newListing.crop_name}
                    onChange={(e) => setNewListing({ ...newListing, crop_name: e.target.value })}
                    required
                  />

                  <Input
                    type="text"
                    label="Location"
                    placeholder="e.g., Monrovia, Nimba County"
                    value={newListing.location}
                    onChange={(e) => setNewListing({ ...newListing, location: e.target.value })}
                    required
                  />
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  <Input
                    type="number"
                    label="Quantity"
                    placeholder="e.g., 50"
                    value={newListing.quantity}
                    onChange={(e) => setNewListing({ ...newListing, quantity: e.target.value })}
                    required
                    min="0"
                    step="0.1"
                  />

                  <div className="form-group">
                    <label className="form-label">Unit</label>
                    <select
                      className="form-input"
                      value={newListing.unit}
                      onChange={(e) => setNewListing({ ...newListing, unit: e.target.value })}
                    >
                      {units.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                      ))}
                    </select>
                  </div>

                  <Input
                    type="number"
                    label="Price per Unit ($)"
                    placeholder="e.g., 2.50"
                    value={newListing.price_per_unit}
                    onChange={(e) => setNewListing({ ...newListing, price_per_unit: e.target.value })}
                    required
                    min="0"
                    step="0.01"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Description (Optional)</label>
                  <textarea
                    className="form-input min-h-24"
                    placeholder="Describe your product quality, farming methods, or any special details..."
                    value={newListing.description}
                    onChange={(e) => setNewListing({ ...newListing, description: e.target.value })}
                    rows={4}
                  />
                </div>

                <div className="flex gap-4">
                  <Button type="submit" variant="primary" isLoading={createLoading}>
                    List Product
                  </Button>
                  <Button 
                    type="button" 
                    variant="ghost" 
                    onClick={() => setShowCreateForm(false)}
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </Card.Body>
          </Card>
        )}

        {/* Market Listings */}
        {filteredListings.length === 0 ? (
          <Card className="text-center py-12">
            <Card.Body>
              <div className="text-6xl mb-4">🛒</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {listings.length === 0 ? 'No Products Listed Yet' : 'No Matching Products'}
              </h3>
              <p className="text-gray-600 mb-6">
                {listings.length === 0 
                  ? 'Be the first to list your agricultural products!'
                  : 'Try adjusting your search or filters to find products.'
                }
              </p>
              {token && listings.length === 0 && (
                <Button variant="primary" onClick={() => setShowCreateForm(true)}>
                  List First Product
                </Button>
              )}
            </Card.Body>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredListings.map((listing) => (
              <Card key={listing.id} className="hover:shadow-medium transition-shadow duration-300">
                <Card.Body className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-900 flex-1">
                      {listing.crop_name}
                    </h3>
                    <div className="text-right ml-4">
                      <div className="text-2xl font-bold text-primary-600">
                        ${listing.price_per_unit}
                      </div>
                      <div className="text-sm text-gray-500">per {listing.unit}</div>
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                      </svg>
                      <span className="font-medium">{listing.quantity} {listing.unit}</span>
                      <span className="ml-1">available</span>
                    </div>

                    <div className="flex items-center text-sm text-gray-600">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      </svg>
                      <span>{listing.location}</span>
                    </div>

                    <div className="flex items-center text-sm text-gray-600">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span>{listing.farmer || 'Community Farmer'}</span>
                    </div>
                  </div>

                  {listing.description && (
                    <p className="text-gray-700 text-sm leading-relaxed mb-4">
                      {listing.description}
                    </p>
                  )}

                  <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>{new Date(listing.created_at).toLocaleDateString()}</span>
                    </div>
                    
                    <Button variant="outline" size="sm">
                      Contact Seller
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            ))}
          </div>
        )}

        {/* Stats */}
        {listings.length > 0 && (
          <div className="mt-12 text-center">
            <div className="inline-flex items-center space-x-6 bg-white rounded-xl shadow-soft border border-gray-200 px-6 py-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-600">{listings.length}</div>
                <div className="text-sm text-gray-600">Products Listed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-secondary-600">{uniqueCrops.length}</div>
                <div className="text-sm text-gray-600">Product Types</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-earth-600">{uniqueLocations.length}</div>
                <div className="text-sm text-gray-600">Locations</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Market;