import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Users, FileText, MessageSquare, Upload, Trash2, LogOut,
    User, ChevronDown, Sparkles, Send, Shield, Briefcase, UserCheck, Building2
} from 'lucide-react';
import api from '../services/api';
import { getUser, logout, isAdmin } from '../utils/auth';
import ProfileModal from '../components/ProfileModal';

// Role configurations
const ROLE_CONFIG = {
    admin: {
        name: 'Administrator',
        color: '#6366f1',
        icon: Shield,
        welcomeMessage: 'You have full access to the system. Manage users, documents, and monitor all activities.'
    },
    manager: {
        name: 'Manager',
        color: '#8b5cf6',
        icon: Briefcase,
        welcomeMessage: 'Welcome! I can help you with team management, reports, and company policies.',
        questions: [
            'Team performance metrics?',
            'Leave approval process?',
            'Budget guidelines?',
            'How to request resources?'
        ]
    },
    hr: {
        name: 'HR',
        color: '#E91E63',
        icon: UserCheck,
        welcomeMessage: 'Welcome to HR Assistant! I can help you with employee management, policies, and recruitment.',
        questions: [
            'Employee onboarding process?',
            'Leave policy details?',
            'Interview guidelines?',
            'Benefits information?'
        ]
    },
    employee: {
        name: 'Employee',
        color: '#22c55e',
        icon: User,
        welcomeMessage: 'Welcome! I\'m here to help you with company policies, leave requests, and general queries.',
        questions: [
            'How to apply for leave?',
            'Work from home policy?',
            'Expense reimbursement?',
            'Training programs?'
        ]
    }
};

function Dashboard() {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [stats, setStats] = useState({ documents: 0, sessions: 0, users: 0 });
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const [showProfileModal, setShowProfileModal] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [selectedDepartment, setSelectedDepartment] = useState('general');

    // Chat state for non-admin view
    const [chatInput, setChatInput] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [chatLoading, setChatLoading] = useState(false);
    const [currentSession, setCurrentSession] = useState(null);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        const userData = getUser();
        if (userData) {
            setUser(userData);
        }
        loadData();
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatMessages]);

    const loadData = async () => {
        setLoading(true);
        try {
            // Load documents
            const docsRes = await api.get('/documents/');
            setDocuments(docsRes.data || []);

            // Load chat sessions
            const sessionsRes = await api.get('/chat/sessions');

            // Update stats
            const newStats = {
                documents: Array.isArray(docsRes.data) ? docsRes.data.length : 0,
                sessions: Array.isArray(sessionsRes.data) ? sessionsRes.data.length : 0,
                users: 0
            };

            // Load users count for admins
            if (isAdmin()) {
                try {
                    const usersRes = await api.get('/users/');
                    newStats.users = Array.isArray(usersRes.data) ? usersRes.data.length : 0;
                } catch (e) {
                    console.log('Could not load users count:', e);
                }
            }

            setStats(newStats);
            console.log('Stats loaded:', newStats);
        } catch (error) {
            console.error('Failed to load data:', error);
        } finally {
            setLoading(false);
        }
    };

    // Chat functions
    const handleSendMessage = async (message) => {
        if (!message?.trim() || chatLoading) return;

        const userMessage = message.trim();
        setChatInput('');
        setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setChatLoading(true);

        try {
            const response = await api.post('/chat/', {
                message: userMessage,
                session_id: currentSession
            });

            setChatMessages(prev => [
                ...prev,
                { role: 'assistant', content: response.data?.response || 'I received your message.' }
            ]);

            if (!currentSession && response.data?.session_id) {
                setCurrentSession(response.data.session_id);
            }
        } catch (error) {
            setChatMessages(prev => [
                ...prev,
                { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
            ]);
        } finally {
            setChatLoading(false);
        }
    };

    const handleChatSubmit = (e) => {
        e.preventDefault();
        handleSendMessage(chatInput);
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploading(true);
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('department', selectedDepartment);

            await api.post('/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            await loadData();
            alert('Document uploaded successfully!');
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Failed to upload document');
        } finally {
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleDeleteDocument = async (docId) => {
        if (!confirm('Are you sure you want to delete this document?')) return;

        try {
            await api.delete(`/documents/${docId}`);
            await loadData();
        } catch (error) {
            console.error('Delete failed:', error);
        }
    };

    const handleLogout = () => {
        logout();
    };

    const getInitials = (name) => {
        return name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U';
    };

    const userRole = user?.role || 'employee';
    const roleConfig = ROLE_CONFIG[userRole] || ROLE_CONFIG.employee;
    const RoleIcon = roleConfig.icon;
    const isAdminUser = userRole === 'admin';

    // ========== NON-ADMIN VIEW (Redirect to Chat) ==========
    if (!isAdminUser) {
        // Redirect non-admin users to the modern chat interface
        navigate('/chat', { replace: true });
        return null;
    }


    // ========== ADMIN VIEW (Full Dashboard) ==========
    return (
        <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
            {/* Navbar */}
            <nav className="navbar">
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                        width: '40px', height: '40px',
                        background: 'var(--gradient-primary)',
                        borderRadius: '10px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center'
                    }}>
                        <Shield size={20} color="white" />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Admin Dashboard</h1>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            Enterprise RAG System
                        </span>
                    </div>
                </div>

                {/* Admin Badge */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 16px',
                    background: 'var(--primary)15',
                    borderRadius: '24px',
                    marginRight: 'auto',
                    marginLeft: '32px'
                }}>
                    <Shield size={16} color="var(--primary)" />
                    <span style={{
                        fontSize: '0.875rem',
                        fontWeight: '600',
                        color: 'var(--primary)',
                        textTransform: 'uppercase'
                    }}>
                        Administrator
                    </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    {/* Profile Dropdown */}
                    <div className="profile-dropdown">
                        <button
                            className="profile-trigger"
                            onClick={() => setShowProfileMenu(!showProfileMenu)}
                        >
                            {user?.profile_photo ? (
                                <img src={user.profile_photo} alt="" className="avatar" style={{ width: '36px', height: '36px' }} />
                            ) : (
                                <div style={{
                                    width: '36px', height: '36px', borderRadius: '50%',
                                    background: 'var(--primary)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    fontWeight: '600', fontSize: '0.875rem', color: 'white'
                                }}>
                                    {getInitials(user?.full_name)}
                                </div>
                            )}
                            <div style={{ textAlign: 'left' }}>
                                <div style={{ fontWeight: '500', fontSize: '0.9rem' }}>{user?.full_name || user?.username}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Administrator</div>
                            </div>
                            <ChevronDown size={16} />
                        </button>

                        {showProfileMenu && (
                            <div className="profile-menu">
                                <button
                                    className="profile-menu-item"
                                    onClick={() => { setShowProfileModal(true); setShowProfileMenu(false); }}
                                >
                                    <User size={18} />
                                    Edit Profile
                                </button>
                                <button
                                    className="profile-menu-item"
                                    onClick={() => { navigate('/chat'); setShowProfileMenu(false); }}
                                >
                                    <MessageSquare size={18} />
                                    AI Chat
                                </button>
                                <button
                                    className="profile-menu-item"
                                    onClick={() => { navigate('/admin/users'); setShowProfileMenu(false); }}
                                >
                                    <Users size={18} />
                                    Manage Users
                                </button>
                                <div style={{ borderTop: '1px solid var(--border-color)', margin: '8px 0' }} />
                                <button className="profile-menu-item danger" onClick={handleLogout}>
                                    <LogOut size={18} />
                                    Logout
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
                {/* Welcome Section */}
                <div style={{ marginBottom: '32px' }}>
                    <h2 style={{ fontSize: '2rem', fontWeight: '700', marginBottom: '8px' }}>
                        Welcome back, {user?.full_name?.split(' ')[0] || user?.username}! 👋
                    </h2>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>
                        Manage your enterprise knowledge base and users
                    </p>
                </div>

                {/* Stats Cards */}
                <div className="dashboard-grid">
                    <div className="stat-card" onClick={() => navigate('/chat')} style={{ cursor: 'pointer' }}>
                        <div className="stat-icon" style={{ background: 'rgba(99, 102, 241, 0.2)' }}>
                            <MessageSquare size={24} color="var(--primary)" />
                        </div>
                        <div className="stat-value" style={{ color: 'var(--primary)' }}>
                            {loading ? '...' : stats.sessions}
                        </div>
                        <div className="stat-label">Chat Sessions</div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon" style={{ background: 'rgba(34, 197, 94, 0.2)' }}>
                            <FileText size={24} color="#22c55e" />
                        </div>
                        <div className="stat-value" style={{ color: '#22c55e' }}>
                            {loading ? '...' : stats.documents}
                        </div>
                        <div className="stat-label">Total Documents</div>
                    </div>

                    <div className="stat-card" onClick={() => navigate('/admin/users')} style={{ cursor: 'pointer' }}>
                        <div className="stat-icon" style={{ background: 'rgba(139, 92, 246, 0.2)' }}>
                            <Users size={24} color="#8b5cf6" />
                        </div>
                        <div className="stat-value" style={{ color: '#8b5cf6' }}>
                            {loading ? '...' : stats.users}
                        </div>
                        <div className="stat-label">Total Users</div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div style={{ marginBottom: '32px' }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '16px' }}>
                        Quick Actions
                    </h3>
                    <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                        <button
                            className="btn btn-primary"
                            onClick={() => navigate('/chat')}
                        >
                            <MessageSquare size={18} />
                            Open AI Chat
                        </button>

                        <button
                            className="btn btn-secondary"
                            onClick={() => fileInputRef.current?.click()}
                            disabled={uploading}
                        >
                            <Upload size={18} />
                            {uploading ? 'Uploading...' : 'Upload Document'}
                        </button>
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileUpload}
                            style={{ display: 'none' }}
                            accept=".pdf,.txt,.doc,.docx"
                        />

                        <button
                            className="btn btn-secondary"
                            onClick={() => navigate('/admin/users')}
                        >
                            <Users size={18} />
                            Manage Users
                        </button>

                        <button
                            className="btn btn-ghost"
                            onClick={loadData}
                            disabled={loading}
                        >
                            🔄 Refresh Stats
                        </button>
                    </div>
                </div>

                {/* Documents Section */}
                <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: '600' }}>
                            All Documents ({documents.length})
                        </h3>
                        <select
                            className="input select"
                            value={selectedDepartment}
                            onChange={(e) => setSelectedDepartment(e.target.value)}
                            style={{ width: 'auto', padding: '8px 32px 8px 12px' }}
                        >
                            <option value="general">General</option>
                            <option value="hr">HR</option>
                            <option value="finance">Finance</option>
                            <option value="it">IT</option>
                            <option value="marketing">Marketing</option>
                            <option value="sales">Sales</option>
                            <option value="operations">Operations</option>
                            <option value="legal">Legal</option>
                        </select>
                    </div>

                    {loading ? (
                        <div className="card" style={{ textAlign: 'center', padding: '48px' }}>
                            <div className="loading-spinner" style={{ margin: '0 auto 16px' }} />
                            <p style={{ color: 'var(--text-muted)' }}>Loading documents...</p>
                        </div>
                    ) : documents.length === 0 ? (
                        <div className="card" style={{ textAlign: 'center', padding: '48px' }}>
                            <FileText size={48} color="var(--text-muted)" style={{ margin: '0 auto 16px' }} />
                            <p style={{ color: 'var(--text-muted)', marginBottom: '16px' }}>
                                No documents uploaded yet.
                            </p>
                            <button
                                className="btn btn-primary"
                                onClick={() => fileInputRef.current?.click()}
                            >
                                <Upload size={18} />
                                Upload First Document
                            </button>
                        </div>
                    ) : (
                        <div className="table-container">
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th>Document</th>
                                        <th>Department</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {documents.map(doc => (
                                        <tr key={doc.id}>
                                            <td>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                                    <FileText size={20} color="var(--text-muted)" />
                                                    <span>{doc.original_filename || doc.filename}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <span className="badge badge-primary">
                                                    {doc.department || 'general'}
                                                </span>
                                            </td>
                                            <td>
                                                <span
                                                    className="badge"
                                                    style={{
                                                        background: doc.status === 'processed' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(251, 191, 36, 0.1)',
                                                        color: doc.status === 'processed' ? '#16a34a' : '#d97706'
                                                    }}
                                                >
                                                    {doc.status}
                                                </span>
                                            </td>
                                            <td>
                                                <button
                                                    className="btn btn-ghost"
                                                    onClick={() => handleDeleteDocument(doc.id)}
                                                    style={{ color: '#ef4444', padding: '8px' }}
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </main>

            {/* Profile Modal */}
            {showProfileModal && (
                <ProfileModal
                    user={user}
                    onClose={() => setShowProfileModal(false)}
                    onUpdate={(updated) => setUser(updated)}
                />
            )}
        </div>
    );
}

export default Dashboard;
