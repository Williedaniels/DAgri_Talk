import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Card } from '../components/ui';

const Home: React.FC = () => {
  const token = localStorage.getItem('access_token');

  const features = [
    {
      icon: '🌾',
      title: 'Traditional Knowledge',
      description: 'Preserve and share ancestral farming wisdom from Liberian elders and experienced farmers. Learn time-tested techniques for sustainable agriculture.',
      link: '/knowledge',
      stats: '500+ Traditional Practices'
    },
    {
      icon: '🛒',
      title: 'Market Connection',
      description: 'Connect farmers directly with buyers and access real-time market prices for your crops. Sell your harvest at fair prices.',
      link: '/market',
      stats: '1000+ Active Listings'
    },
    {
      icon: '🤝',
      title: 'Community Support',
      description: 'Learn from fellow farmers and experts through our community platform. Get advice, share experiences, and grow together.',
      link: token ? '/knowledge' : '/register',
      stats: '2500+ Community Members'
    }
  ];

  const stats = [
    { number: '2,500+', label: 'Farmers Connected' },
    { number: '500+', label: 'Knowledge Entries' },
    { number: '1,000+', label: 'Market Listings' },
    { number: '50+', label: 'Communities Served' },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-secondary-50 section-padding">
        <div className="container-custom">
          <div className="text-center max-w-4xl mx-auto">
            <div className="animate-fade-in">
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
                Welcome to{' '}
                <span className="text-gradient">D'Agri Talk</span>
              </h1>
              <p className="text-xl lg:text-2xl text-gray-600 mb-4 font-serif">
                Traditional Agricultural Knowledge Platform for Liberia
              </p>
              <p className="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
                Connecting farmers, preserving wisdom, building communities. 
                Join thousands of farmers sharing knowledge and growing together.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                {token ? (
                  <>
                    <Link to="/knowledge">
                      <Button variant="primary" size="lg" className="w-full sm:w-auto">
                        Explore Knowledge 📚
                      </Button>
                    </Link>
                    <Link to="/market">
                      <Button variant="outline" size="lg" className="w-full sm:w-auto">
                        Browse Market 🛒
                      </Button>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link to="/register">
                      <Button variant="primary" size="lg" className="w-full sm:w-auto">
                        Get Started Free
                      </Button>
                    </Link>
                    <Link to="/login">
                      <Button variant="outline" size="lg" className="w-full sm:w-auto">
                        Sign In
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center animate-slide-up">
                <div className="text-3xl lg:text-4xl font-bold text-primary-600 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600 text-sm lg:text-base">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section-padding bg-gray-50 bg-pattern">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Empowering Liberian Agriculture
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover powerful tools designed specifically for Liberian farmers 
              to preserve traditions, access markets, and build stronger communities.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-medium transition-shadow duration-300 animate-slide-up group">
                <Card.Body className="p-8">
                  <div className="text-6xl mb-6 group-hover:animate-bounce-gentle">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    {feature.description}
                  </p>
                  <div className="text-sm text-primary-600 font-medium mb-6">
                    {feature.stats}
                  </div>
                  <Link to={feature.link}>
                    <Button 
                      variant={index === 0 ? 'primary' : 'outline'} 
                      size="sm" 
                      className="w-full"
                    >
                      Learn More
                    </Button>
                  </Link>
                </Card.Body>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-gradient-to-r from-primary-600 to-primary-700">
        <div className="container-custom text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
              Ready to Join Our Growing Community?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Connect with fellow farmers, share your knowledge, and access the marketplace. 
              It's free to get started!
            </p>
            
            {!token && (
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/register">
                  <Button variant="secondary" size="lg" className="w-full sm:w-auto">
                    Create Account
                  </Button>
                </Link>
                <Link to="/knowledge">
                  <Button variant="outline" size="lg" className="w-full sm:w-auto text-white border-white hover:bg-white hover:text-primary-600">
                    Explore Knowledge
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container-custom">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 text-2xl font-bold mb-4">
              <span className="text-3xl">🌾</span>
              <span>D'Agri Talk</span>
            </div>
            <p className="text-gray-400 mb-8">
              Connecting Liberian farmers with knowledge, markets, and community
            </p>
            <div className="flex justify-center space-x-8 text-sm">
              <Link to="/knowledge" className="text-gray-400 hover:text-white transition-colors">
                Knowledge Hub
              </Link>
              <Link to="/market" className="text-gray-400 hover:text-white transition-colors">
                Marketplace
              </Link>
              {!token && (
                <>
                  <Link to="/login" className="text-gray-400 hover:text-white transition-colors">
                    Login
                  </Link>
                  <Link to="/register" className="text-gray-400 hover:text-white transition-colors">
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;