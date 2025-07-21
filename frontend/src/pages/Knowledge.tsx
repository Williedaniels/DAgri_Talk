import React, { useState, useEffect } from 'react';
import { knowledgeAPI } from '../services/api';
import { KnowledgeEntry } from '../types';
import { Button, Card, Alert, Input } from '../components/ui';

const Knowledge: React.FC = () => {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('all');
  const [selectedLanguage, setSelectedLanguage] = useState('all');

  const [newEntry, setNewEntry] = useState({
    title: '',
    content: '',
    crop_type: '',
    language: 'English',
  });

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const response = await knowledgeAPI.getAll();
      // If API returns empty data, use mock data for demonstration
      if (!response.data || response.data.length === 0) {
      const mockData = [
        {
          id: 1,
          title: "Traditional Rice Planting in Liberia",
          content: "Our ancestors taught us to plant rice during the rainy season. Start by preparing the land with traditional tools, then soak the seeds for 24 hours before planting. Plant in rows with proper spacing for better yield.",
          crop_type: "Rice",
          language: "English",
          season: "Rainy Season",
          region: "Bong County",
          author: "Elder Joseph Kpan",
          created_at: "2024-01-15T08:00:00Z",
          updated_at: "2024-01-15T08:00:00Z"
        },
        {
          id: 2,
          title: "Palm Oil Processing Techniques",
          content: "Traditional palm oil extraction requires patience and skill. Harvest ripe palm fruits when they turn red-orange. Boil the fruits for 2-3 hours, then pound to separate the oil. This method produces pure, high-quality oil.",
          crop_type: "Palm Oil",
          language: "English",
          season: "All Year",
          region: "Grand Bassa County",
          author: "Mama Sarah Togba",
          created_at: "2024-01-20T10:30:00Z",
          updated_at: "2024-01-20T10:30:00Z"
        },
        {
          id: 3,
          title: "Cassava Farming Best Practices",
          content: "Cassava grows well in our soil. Plant during the dry season, choose healthy stems about 20cm long. Plant at an angle in well-drained soil. Weed regularly and harvest after 8-12 months when leaves start yellowing.",
          crop_type: "Cassava",
          language: "English",
          season: "Dry Season",
          region: "Nimba County",
          author: "Farmer John Pewee",
          created_at: "2024-02-01T14:20:00Z",
          updated_at: "2024-02-01T14:20:00Z"
        },
        {
          id: 4,
          title: "Natural Pest Control Methods",
          content: "Use neem leaves and soap water to control pests naturally. Crush neem leaves, mix with water and small soap, spray on crops early morning. This traditional method is safe and effective for protecting vegetables.",
          crop_type: "Vegetables",
          language: "English",
          season: "All Year",
          region: "Montserrado County",
          author: "Elder Mary Kollie",
          created_at: "2024-02-10T09:15:00Z",
          updated_at: "2024-02-10T09:15:00Z"
        },
        {
          id: 5,
          title: "Cocoa Cultivation Wisdom",
          content: "Plant cocoa under shade trees for better growth. Our elders planted cocoa with kola nut trees for natural protection. Regular pruning and proper spacing between trees ensures good air circulation and healthy pods.",
          crop_type: "Cocoa",
          language: "English",
          season: "All Year",
          region: "Maryland County",
          author: "Chief Farmer Moses Gaye",
          created_at: "2024-02-15T16:45:00Z",
          updated_at: "2024-02-15T16:45:00Z"
        }
      ];
      setEntries(mockData);
      setError('Using sample knowledge entries for demonstration');
      } else {
        setEntries(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch knowledge entries:', error);
      setError('Failed to load knowledge entries');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEntry = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      setError('Please login to share knowledge');
      return;
    }

    setCreateLoading(true);
    setError('');

    try {
      await knowledgeAPI.create(newEntry);
      setSuccess('Knowledge entry created successfully!');
      setNewEntry({ title: '', content: '', crop_type: '', language: 'English' });
      setShowCreateForm(false);
      fetchEntries(); // Refresh the list
      setTimeout(() => setSuccess(''), 3000);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to create knowledge entry');
    } finally {
      setCreateLoading(false);
    }
  };

  // Filter entries based on search and filters
  const filteredEntries = entries.filter(entry => {
    const matchesSearch = entry.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         entry.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         entry.crop_type.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCrop = selectedCrop === 'all' || entry.crop_type.toLowerCase().includes(selectedCrop.toLowerCase());
    const matchesLanguage = selectedLanguage === 'all' || entry.language.toLowerCase() === selectedLanguage.toLowerCase();
    
    return matchesSearch && matchesCrop && matchesLanguage;
  });

  const uniqueCrops = Array.from(new Set(entries.map(entry => entry.crop_type).filter(Boolean)));
  const uniqueLanguages = Array.from(new Set(entries.map(entry => entry.language)));

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container-custom">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading traditional knowledge...</p>
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
            📚 Traditional Agricultural Knowledge
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover time-tested farming wisdom from Liberian elders and experienced farmers. 
            Share your knowledge to help preserve our agricultural heritage.
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
                  placeholder="Search knowledge entries..."
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
                  <option value="all">All Crops</option>
                  {uniqueCrops.map(crop => (
                    <option key={crop} value={crop}>{crop}</option>
                  ))}
                </select>

                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="form-input w-auto"
                >
                  <option value="all">All Languages</option>
                  {uniqueLanguages.map(language => (
                    <option key={language} value={language}>{language}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Share Knowledge Button */}
            {token && (
              <Button
                variant="primary"
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="w-full sm:w-auto"
              >
                {showCreateForm ? 'Cancel' : '✨ Share Knowledge'}
              </Button>
            )}
            
            {!token && (
              <p className="text-sm text-gray-500 text-center">
                <a href="/login" className="text-primary-600 hover:text-primary-700">Login</a> to share knowledge
              </p>
            )}
          </div>
        </div>

        {/* Create Knowledge Form */}
        {showCreateForm && token && (
          <Card className="mb-8 animate-fade-in">
            <Card.Header>
              <h3 className="text-lg font-semibold text-gray-900">Share Your Knowledge</h3>
              <p className="text-sm text-gray-600">Help preserve traditional farming wisdom for future generations</p>
            </Card.Header>
            <Card.Body>
              <form onSubmit={handleCreateEntry} className="space-y-6">
                <Input
                  type="text"
                  label="Title"
                  placeholder="e.g., Traditional Rice Planting Techniques"
                  value={newEntry.title}
                  onChange={(e) => setNewEntry({ ...newEntry, title: e.target.value })}
                  required
                />

                <div className="form-group">
                  <label className="form-label">Content</label>
                  <textarea
                    className="form-input min-h-32"
                    placeholder="Share your traditional farming knowledge, techniques, or wisdom..."
                    value={newEntry.content}
                    onChange={(e) => setNewEntry({ ...newEntry, content: e.target.value })}
                    required
                    rows={6}
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <Input
                    type="text"
                    label="Crop Type"
                    placeholder="e.g., Rice, Cassava, Palm Oil"
                    value={newEntry.crop_type}
                    onChange={(e) => setNewEntry({ ...newEntry, crop_type: e.target.value })}
                  />

                  <div className="form-group">
                    <label className="form-label">Language</label>
                    <select
                      className="form-input"
                      value={newEntry.language}
                      onChange={(e) => setNewEntry({ ...newEntry, language: e.target.value })}
                    >
                      <option value="English">English</option>
                      <option value="Kpelle">Kpelle</option>
                      <option value="Bassa">Bassa</option>
                      <option value="Gio">Gio</option>
                      <option value="Mano">Mano</option>
                      <option value="Loma">Loma</option>
                      <option value="Krahn">Krahn</option>
                      <option value="Vai">Vai</option>
                      <option value="Gola">Gola</option>
                      <option value="Mandingo">Mandingo</option>
                      <option value="Gbandi">Gbandi</option>
                    </select>
                  </div>
                </div>

                <div className="flex gap-4">
                  <Button type="submit" variant="primary" isLoading={createLoading}>
                    Share Knowledge
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

        {/* Knowledge Entries */}
        {filteredEntries.length === 0 ? (
          <Card className="text-center py-12">
            <Card.Body>
              <div className="text-6xl mb-4">📚</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {entries.length === 0 ? 'No Knowledge Entries Yet' : 'No Matching Entries'}
              </h3>
              <p className="text-gray-600 mb-6">
                {entries.length === 0 
                  ? 'Be the first to share traditional farming wisdom!'
                  : 'Try adjusting your search or filters to find relevant knowledge.'
                }
              </p>
              {token && entries.length === 0 && (
                <Button variant="primary" onClick={() => setShowCreateForm(true)}>
                  Share First Knowledge Entry
                </Button>
              )}
            </Card.Body>
          </Card>
        ) : (
          <div className="grid gap-6">
            {filteredEntries.map((entry) => (
              <Card key={entry.id} className="hover:shadow-medium transition-shadow duration-300">
                <Card.Body className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-900 flex-1">
                      {entry.title}
                    </h3>
                    <div className="flex items-center space-x-2 text-sm text-gray-500 ml-4">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {new Date(entry.created_at).toLocaleDateString()}
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {entry.crop_type && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        🌾 {entry.crop_type}
                      </span>
                    )}
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary-100 text-secondary-800">
                      🗣️ {entry.language}
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-earth-100 text-earth-800">
                      👤 {entry.author || 'Community Member'}
                    </span>
                  </div>

                  <p className="text-gray-700 leading-relaxed">
                    {entry.content}
                  </p>
                </Card.Body>
              </Card>
            ))}
          </div>
        )}

        {/* Stats */}
        {entries.length > 0 && (
          <div className="mt-12 text-center">
            <div className="inline-flex items-center space-x-6 bg-white rounded-xl shadow-soft border border-gray-200 px-6 py-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-600">{entries.length}</div>
                <div className="text-sm text-gray-600">Knowledge Entries</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-secondary-600">{uniqueCrops.length}</div>
                <div className="text-sm text-gray-600">Crop Types</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-earth-600">{uniqueLanguages.length}</div>
                <div className="text-sm text-gray-600">Languages</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Knowledge;