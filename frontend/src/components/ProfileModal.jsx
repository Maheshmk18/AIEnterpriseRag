import { useState, useRef } from 'react';
import { X, Camera, Mail, Phone, User, Lock, Save } from 'lucide-react';
import api from '../services/api';

const ProfileModal = ({ user, onClose, onUpdate }) => {
    const [formData, setFormData] = useState({
        full_name: user?.full_name || '',
        email: user?.email || '',
        phone: user?.phone || '',
        password: '',
        confirmPassword: ''
    });
    const [profilePhoto, setProfilePhoto] = useState(user?.profile_photo || null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const fileInputRef = useRef(null);

    const handlePhotoChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) {
                setError('Image must be less than 5MB');
                return;
            }

            const reader = new FileReader();
            reader.onloadend = () => {
                setProfilePhoto(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (formData.password && formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            const updateData = {
                full_name: formData.full_name,
                email: formData.email,
                phone: formData.phone,
                profile_photo: profilePhoto
            };

            if (formData.password) {
                updateData.password = formData.password;
            }

            const response = await api.put('/users/me', updateData);

            // Update local storage
            const userData = JSON.parse(localStorage.getItem('user') || '{}');
            const updatedUser = { ...userData, ...response.data };
            localStorage.setItem('user', JSON.stringify(updatedUser));

            setSuccess('Profile updated successfully!');
            onUpdate && onUpdate(response.data);

            setTimeout(() => {
                onClose();
            }, 1500);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to update profile');
        } finally {
            setLoading(false);
        }
    };

    const getInitials = (name) => {
        return name
            ?.split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2) || 'U';
    };

    const getRoleColor = (role) => {
        const colors = {
            admin: '#9C27B0',
            manager: '#FF9800',
            hr: '#E91E63',
            employee: '#2196F3'
        };
        return colors[role] || '#6366f1';
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: '600' }}>Edit Profile</h2>
                    <button onClick={onClose} className="btn-ghost" style={{ padding: '8px' }}>
                        <X size={20} />
                    </button>
                </div>

                {error && (
                    <div style={{
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

                {success && (
                    <div style={{
                        padding: '12px 16px',
                        background: 'rgba(34, 197, 94, 0.1)',
                        border: '1px solid rgba(34, 197, 94, 0.3)',
                        borderRadius: '8px',
                        color: '#22c55e',
                        marginBottom: '16px'
                    }}>
                        {success}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    {/* Profile Photo */}
                    <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                        <div style={{ position: 'relative', display: 'inline-block' }}>
                            {profilePhoto ? (
                                <img
                                    src={profilePhoto}
                                    alt="Profile"
                                    style={{
                                        width: '100px',
                                        height: '100px',
                                        borderRadius: '50%',
                                        objectFit: 'cover',
                                        border: `3px solid ${getRoleColor(user?.role)}`
                                    }}
                                />
                            ) : (
                                <div
                                    style={{
                                        width: '100px',
                                        height: '100px',
                                        borderRadius: '50%',
                                        background: `linear-gradient(135deg, ${getRoleColor(user?.role)}, ${getRoleColor(user?.role)}cc)`,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontSize: '2rem',
                                        fontWeight: '600',
                                        color: 'white'
                                    }}
                                >
                                    {getInitials(user?.full_name)}
                                </div>
                            )}
                            <button
                                type="button"
                                onClick={() => fileInputRef.current?.click()}
                                style={{
                                    position: 'absolute',
                                    bottom: '0',
                                    right: '0',
                                    width: '32px',
                                    height: '32px',
                                    borderRadius: '50%',
                                    background: 'var(--primary)',
                                    border: '2px solid var(--bg-secondary)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    cursor: 'pointer',
                                    color: 'white'
                                }}
                            >
                                <Camera size={16} />
                            </button>
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/*"
                                onChange={handlePhotoChange}
                                style={{ display: 'none' }}
                            />
                        </div>
                        <p style={{ marginTop: '8px', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                            Click to upload photo (max 5MB)
                        </p>
                    </div>

                    {/* Form Fields */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <div className="input-group">
                            <label className="input-label">
                                <User size={14} style={{ marginRight: '6px', display: 'inline' }} />
                                Full Name
                            </label>
                            <input
                                type="text"
                                className="input"
                                value={formData.full_name}
                                onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                                placeholder="Your full name"
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">
                                <Mail size={14} style={{ marginRight: '6px', display: 'inline' }} />
                                Email Address
                            </label>
                            <input
                                type="email"
                                className="input"
                                value={formData.email}
                                onChange={e => setFormData({ ...formData, email: e.target.value })}
                                placeholder="your.email@company.com"
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">
                                <Phone size={14} style={{ marginRight: '6px', display: 'inline' }} />
                                Phone Number
                            </label>
                            <input
                                type="tel"
                                className="input"
                                value={formData.phone}
                                onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                placeholder="+1 234 567 8900"
                            />
                        </div>

                        <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '16px', marginTop: '8px' }}>
                            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
                                Change Password (leave blank to keep current)
                            </p>

                            <div className="input-group" style={{ marginBottom: '16px' }}>
                                <label className="input-label">
                                    <Lock size={14} style={{ marginRight: '6px', display: 'inline' }} />
                                    New Password
                                </label>
                                <input
                                    type="password"
                                    className="input"
                                    value={formData.password}
                                    onChange={e => setFormData({ ...formData, password: e.target.value })}
                                    placeholder="••••••••"
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">
                                    <Lock size={14} style={{ marginRight: '6px', display: 'inline' }} />
                                    Confirm Password
                                </label>
                                <input
                                    type="password"
                                    className="input"
                                    value={formData.confirmPassword}
                                    onChange={e => setFormData({ ...formData, confirmPassword: e.target.value })}
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary"
                            disabled={loading}
                            style={{ marginTop: '8px', width: '100%' }}
                        >
                            {loading ? (
                                <>
                                    <div className="loading-spinner" />
                                    Saving...
                                </>
                            ) : (
                                <>
                                    <Save size={18} />
                                    Save Changes
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ProfileModal;
