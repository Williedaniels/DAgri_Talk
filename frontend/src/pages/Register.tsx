import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { Button, Input, Card, Alert } from '../components/ui';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    user_type: 'farmer',
    location: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { username, email, password, user_type, location } = formData;

  const onChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await authAPI.register({
        username,
        email,
        password,
        user_type,
        location: location || undefined,
      });
      
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.message || 'An error occurred during registration.');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  const userTypes = [
    { value: 'farmer', label: '🌾 Farmer', desc: 'Growing crops and livestock' },
    { value: 'elder', label: '👴 Elder', desc: 'Sharing traditional knowledge' },
    { value: 'buyer', label: '🛒 Buyer', desc: 'Purchasing agricultural products' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <span className="text-4xl">🌾</span>
            <h1 className="text-2xl font-bold text-gradient">D'Agri Talk</h1>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Join Our Community
          </h2>
          <p className="text-gray-600">
            Create your account to start sharing knowledge and connecting with farmers
          </p>
        </div>

        {/* Registration Card */}
        <Card className="animate-fade-in">
          <Card.Body className="p-8">
            <form onSubmit={onSubmit} className="space-y-6">
              <Input
                type="text"
                label="Username"
                name="username"
                placeholder="Choose a unique username"
                value={username}
                onChange={onChange}
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                }
                required
              />

              <Input
                type="email"
                label="Email Address"
                name="email"
                placeholder="Enter your email address"
                value={email}
                onChange={onChange}
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                }
                required
              />

              <Input
                type="password"
                label="Password"
                name="password"
                placeholder="Create a strong password"
                value={password}
                onChange={onChange}
                hint="Must be at least 6 characters long"
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                }
                minLength={6}
                required
              />

              <div className="form-group">
                <label className="form-label">I am a...</label>
                <div className="grid grid-cols-1 gap-2">
                  {userTypes.map((type) => (
                    <label
                      key={type.value}
                      className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                        user_type === type.value
                          ? 'border-primary-500 bg-primary-50 text-primary-700'
                          : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
                      }`}
                    >
                      <input
                        type="radio"
                        name="user_type"
                        value={type.value}
                        checked={user_type === type.value}
                        onChange={onChange}
                        className="sr-only"
                      />
                      <div className="flex-1">
                        <div className="font-medium">{type.label}</div>
                        <div className="text-sm text-gray-500">{type.desc}</div>
                      </div>
                      {user_type === type.value && (
                        <svg className="w-5 h-5 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      )}
                    </label>
                  ))}
                </div>
              </div>

              <Input
                type="text"
                label="Location (Optional)"
                name="location"
                placeholder="e.g., Monrovia, Liberia"
                value={location}
                onChange={onChange}
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                }
              />

              {error && (
                <Alert type="error">
                  {error}
                </Alert>
              )}

              {success && (
                <Alert type="success">
                  {success}
                </Alert>
              )}

              <Button
                type="submit"
                variant="primary"
                size="lg"
                isLoading={loading}
                className="w-full"
              >
                Create Account
              </Button>
            </form>
          </Card.Body>

          <Card.Footer className="text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link
                to="/login"
                className="text-primary-600 hover:text-primary-700 font-medium transition-colors"
              >
                Sign in here
              </Link>
            </p>
          </Card.Footer>
        </Card>

        {/* Terms */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            By creating an account, you agree to connect with farmers and share knowledge responsibly.{' '}
            <Link
              to="/"
              className="text-primary-600 hover:text-primary-700 transition-colors"
            >
              Learn more about our platform
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;

