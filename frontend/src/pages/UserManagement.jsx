import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit2, Trash2, Check, X, Plus, Users, Home } from 'lucide-react';
import api from '../services/api';
import { getUser } from '../utils/auth';

const ROLES = [
  { id: 'admin', name: 'Administrator' },
  { id: 'manager', name: 'Manager' },
  { id: 'hr', name: 'HR' },
  { id: 'employee', name: 'Employee' }
];

function UserManagement() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [editingUser, setEditingUser] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createForm, setCreateForm] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'employee'
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const response = await api.get('/users/');
      setUsers(response.data || []);
    } catch (err) {
      console.error('Failed to load users:', err);
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user.id);
    setEditForm({
      email: user.email,
      full_name: user.full_name || '',
      is_active: user.is_active,
      role: user.role
    });
  };

  const handleSave = async (userId) => {
    try {
      await api.put(`/users/${userId}`, editForm);
      setEditingUser(null);
      setSuccess('User updated successfully');
      setTimeout(() => setSuccess(''), 3000);
      await loadUsers();
    } catch (err) {
      setError('Failed to update user: ' + (err.response?.data?.detail || err.message));
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleDelete = async (userId) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    try {
      await api.delete(`/users/${userId}`);
      setSuccess('User deleted successfully');
      setTimeout(() => setSuccess(''), 3000);
      await loadUsers();
    } catch (err) {
      setError('Failed to delete user: ' + (err.response?.data?.detail || err.message));
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/users/', createForm);
      setShowCreateModal(false);
      setCreateForm({ username: '', email: '', password: '', full_name: '', role: 'employee' });
      setSuccess('User created successfully');
      setTimeout(() => setSuccess(''), 3000);
      await loadUsers();
    } catch (err) {
      setError('Failed to create user: ' + (err.response?.data?.detail || err.message));
    }
  };



  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {/* Header */}
      <div className="navbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-ghost"
            style={{ padding: '8px' }}
          >
            <ArrowLeft size={24} />
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px', height: '40px',
              background: 'var(--gradient-primary)',
              borderRadius: '10px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Users size={20} color="white" />
            </div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: '600' }}>User Management</h1>
          </div>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary"
        >
          <Plus size={18} />
          Create User
        </button>
      </div>

      {/* Content */}
      <div style={{ padding: '32px', maxWidth: '1200px', margin: '0 auto' }}>
        {/* Alerts */}
        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {/* Users Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', padding: '48px' }}>
                    <div className="loading-spinner" style={{ margin: '0 auto' }} />
                  </td>
                </tr>
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', padding: '48px', color: 'var(--text-muted)' }}>
                    No users found
                  </td>
                </tr>
              ) : (
                users.map(user => (
                  <tr key={user.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                          width: '40px', height: '40px', borderRadius: '50%',
                          background: 'var(--primary)',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          color: 'white', fontWeight: '600', fontSize: '0.875rem'
                        }}>
                          {user.full_name?.charAt(0) || user.username?.charAt(0) || 'U'}
                        </div>
                        <div>
                          <div style={{ fontWeight: '500' }}>{user.full_name || user.username}</div>
                          <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>@{user.username}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      {editingUser === user.id ? (
                        <input
                          type="email"
                          className="input"
                          value={editForm.email}
                          onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                          style={{ width: '200px' }}
                        />
                      ) : (
                        user.email
                      )}
                    </td>
                    <td>
                      {editingUser === user.id ? (
                        <select
                          className="input"
                          value={editForm.role}
                          onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                        >
                          {ROLES.map(r => (
                            <option key={r.id} value={r.id}>{r.name}</option>
                          ))}
                        </select>
                      ) : (
                        <span className="badge" style={{ background: 'var(--primary)', color: 'white' }}>
                          {user.role}
                        </span>
                      )}
                    </td>
                    <td>
                      <span
                        className="badge"
                        style={{
                          background: user.is_active ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                          color: user.is_active ? '#16a34a' : '#dc2626'
                        }}
                      >
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        {editingUser === user.id ? (
                          <>
                            <button
                              onClick={() => handleSave(user.id)}
                              className="btn btn-ghost"
                              style={{ color: '#16a34a', padding: '8px' }}
                            >
                              <Check size={18} />
                            </button>
                            <button
                              onClick={() => setEditingUser(null)}
                              className="btn btn-ghost"
                              style={{ color: '#dc2626', padding: '8px' }}
                            >
                              <X size={18} />
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              onClick={() => handleEdit(user)}
                              className="btn btn-ghost"
                              style={{ padding: '8px' }}
                            >
                              <Edit2 size={18} />
                            </button>
                            <button
                              onClick={() => handleDelete(user.id)}
                              className="btn btn-ghost"
                              style={{ color: '#dc2626', padding: '8px' }}
                            >
                              <Trash2 size={18} />
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create User Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '24px' }}>
              Create New User
            </h2>

            {error && <div className="alert alert-error">{error}</div>}

            <form onSubmit={handleCreate}>
              <div className="input-group" style={{ marginBottom: '16px' }}>
                <label className="input-label">Username *</label>
                <input
                  type="text"
                  className="input"
                  value={createForm.username}
                  onChange={(e) => setCreateForm({ ...createForm, username: e.target.value })}
                  required
                  placeholder="Enter username"
                />
              </div>

              <div className="input-group" style={{ marginBottom: '16px' }}>
                <label className="input-label">Full Name</label>
                <input
                  type="text"
                  className="input"
                  value={createForm.full_name}
                  onChange={(e) => setCreateForm({ ...createForm, full_name: e.target.value })}
                  placeholder="Enter full name"
                />
              </div>

              <div className="input-group" style={{ marginBottom: '16px' }}>
                <label className="input-label">Email *</label>
                <input
                  type="email"
                  className="input"
                  value={createForm.email}
                  onChange={(e) => setCreateForm({ ...createForm, email: e.target.value })}
                  required
                  placeholder="Enter email"
                />
              </div>

              <div className="input-group" style={{ marginBottom: '16px' }}>
                <label className="input-label">Password *</label>
                <input
                  type="password"
                  className="input"
                  value={createForm.password}
                  onChange={(e) => setCreateForm({ ...createForm, password: e.target.value })}
                  required
                  placeholder="Enter password"
                />
              </div>

              <div className="input-group" style={{ marginBottom: '24px' }}>
                <label className="input-label">Role</label>
                <select
                  className="input select"
                  value={createForm.role}
                  onChange={(e) => setCreateForm({ ...createForm, role: e.target.value })}
                >
                  {ROLES.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  <Plus size={18} />
                  Create User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserManagement;
