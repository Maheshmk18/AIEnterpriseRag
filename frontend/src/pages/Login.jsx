import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, Eye, EyeOff, Sparkles, TestTube } from 'lucide-react';
import api from '../services/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showTestCredentials, setShowTestCredentials] = useState(false);
  const navigate = useNavigate();

  const testAccounts = [
    { role: 'Admin', username: 'admin', password: 'admin123', color: '#9C27B0' },
    { role: 'HR', username: 'hr', password: '1234', color: '#E91E63' },
    { role: 'Manager', username: 'manager', password: '12345', color: '#FF9800' },
    { role: 'Employee', username: 'employee', password: '123456', color: '#2196F3' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      localStorage.setItem('token', response.data.access_token);

      const userResponse = await api.get('/users/me');
      localStorage.setItem('user', JSON.stringify(userResponse.data));

      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const fillCredentials = (account) => {
    setUsername(account.username);
    setPassword(account.password);
    setShowTestCredentials(false);
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Animated Background Circles */}
      <div style={{
        position: 'absolute',
        top: '-10%',
        right: '-5%',
        width: '500px',
        height: '500px',
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '50%',
        animation: 'float 6s ease-in-out infinite'
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: '-10%',
        left: '-5%',
        width: '400px',
        height: '400px',
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '50%',
        animation: 'float 8s ease-in-out infinite reverse'
      }}></div>

      <div className="flex flex-col md:flex-row w-full max-w-4xl bg-white rounded-3xl overflow-hidden shadow-2xl relative z-10">
        {/* Left Side - Branding */}
        <div className="flex-1 p-8 md:p-12 flex flex-col justify-center text-white" style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            background: 'rgba(255,255,255,0.2)',
            borderRadius: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '24px',
            animation: 'pulse 2s ease-in-out infinite'
          }}>
            <Sparkles size={32} />
          </div>
          <h1 className="text-3xl font-bold mb-3">
            Enterprise RAG
          </h1>
          <p className="opacity-90 text-lg leading-relaxed">
            AI-powered knowledge management for your organization
          </p>
          <div className="mt-8 hidden md:block">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ width: '8px', height: '8px', background: 'rgba(255,255,255,0.8)', borderRadius: '50%' }} />
              <span style={{ opacity: 0.9 }}>Instant answers from your documents</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ width: '8px', height: '8px', background: 'rgba(255,255,255,0.8)', borderRadius: '50%' }} />
              <span style={{ opacity: 0.9 }}>Secure, role-based access</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ width: '8px', height: '8px', background: 'rgba(255,255,255,0.8)', borderRadius: '50%' }} />
              <span style={{ opacity: 0.9 }}>Powered by advanced AI</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="flex-1 p-8 md:p-12 flex flex-col justify-center">
          <h2 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '8px', color: '#1e293b' }}>
            Welcome back
          </h2>
          <p style={{ color: '#64748b', marginBottom: '32px' }}>
            Sign in to access your dashboard
          </p>

          {error && (
            <div className="alert alert-error" style={{
              padding: '12px 16px',
              background: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              borderRadius: '8px',
              color: '#ef4444',
              marginBottom: '16px'
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="input-group" style={{ marginBottom: '20px' }}>
              <label className="input-label">Username</label>
              <input
                type="text"
                className="input"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="input-group" style={{ marginBottom: '24px' }}>
              <label className="input-label">Password</label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="input"
                  style={{ width: '100%', paddingRight: '48px' }}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#64748b',
                    padding: '8px'
                  }}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              style={{ width: '100%', padding: '14px', fontSize: '1rem' }}
            >
              {loading ? (
                <>
                  <div className="loading-spinner" />
                  Signing in...
                </>
              ) : (
                <>
                  <LogIn size={20} />
                  Sign In
                </>
              )}
            </button>
          </form>

          {/* Test Credentials Button */}
          <div style={{ marginTop: '24px', borderTop: '1px solid #e2e8f0', paddingTop: '24px' }}>
            <button
              onClick={() => setShowTestCredentials(!showTestCredentials)}
              style={{
                width: '100%',
                padding: '12px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '0.95rem',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.4)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
              }}
            >
              <TestTube size={18} />
              {showTestCredentials ? 'Hide' : 'Try'} Test Credentials
            </button>

            {/* Test Credentials Dropdown */}
            {showTestCredentials && (
              <div style={{
                marginTop: '16px',
                background: '#f8fafc',
                borderRadius: '12px',
                padding: '16px',
                animation: 'slideDown 0.3s ease-out'
              }}>
                <p style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '12px', fontWeight: '500' }}>
                  Click to auto-fill credentials:
                </p>
                <div style={{ display: 'grid', gap: '8px' }}>
                  {testAccounts.map((account, index) => (
                    <button
                      key={index}
                      onClick={() => fillCredentials(account)}
                      style={{
                        padding: '12px 16px',
                        background: 'white',
                        border: `2px solid ${account.color}20`,
                        borderRadius: '8px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px'
                      }}
                      onMouseOver={(e) => {
                        e.currentTarget.style.borderColor = account.color;
                        e.currentTarget.style.background = `${account.color}10`;
                        e.currentTarget.style.transform = 'translateX(4px)';
                      }}
                      onMouseOut={(e) => {
                        e.currentTarget.style.borderColor = `${account.color}20`;
                        e.currentTarget.style.background = 'white';
                        e.currentTarget.style.transform = 'translateX(0)';
                      }}
                    >
                      <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: account.color
                      }}></div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: '600', color: '#1e293b', fontSize: '0.9rem' }}>
                          {account.role}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                          {account.username} / {account.password}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <p style={{
            marginTop: '24px',
            textAlign: 'center',
            color: '#94a3b8',
            fontSize: '0.875rem'
          }}>
            Contact your administrator for account access
          </p>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default Login;
