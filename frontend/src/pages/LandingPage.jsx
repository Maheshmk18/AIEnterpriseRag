import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Sparkles, Upload, MessageSquare, ArrowRight,
    Brain, FileText, Link2, Shield, Zap, Clock,
    Users, Building2, DollarSign, Code, Settings,
    Menu, X, ChevronDown, CheckCircle, Play, Linkedin
} from 'lucide-react';

function LandingPage() {
    const navigate = useNavigate();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [scrollY, setScrollY] = useState(0);
    const [activeDemo, setActiveDemo] = useState(0);

    useEffect(() => {
        const handleScroll = () => setScrollY(window.scrollY);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveDemo((prev) => (prev + 1) % 3);
        }, 4000);
        return () => clearInterval(interval);
    }, []);

    const scrollToSection = (id) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
        setMobileMenuOpen(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#F8F7FF] via-white to-[#ECEBFF]">
            {/* Navigation */}
            <nav style={{
                position: 'fixed',
                top: 0,
                width: '100%',
                background: scrollY > 50 ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.8)',
                backdropFilter: 'blur(12px)',
                borderBottom: '1px solid rgba(108,99,255,0.1)',
                zIndex: 50,
                transition: 'all 0.3s ease',
                boxShadow: scrollY > 50 ? '0 4px 20px rgba(108,99,255,0.08)' : 'none'
            }}>
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div style={{
                                width: '44px',
                                height: '44px',
                                background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                boxShadow: '0 4px 12px rgba(108,99,255,0.3)'
                            }}>
                                <Sparkles className="text-white" size={22} />
                            </div>
                            <span className="text-xl font-bold bg-gradient-to-r from-[#6C63FF] to-[#7A5AF8] bg-clip-text text-transparent">
                                AI Enterprise RAG
                            </span>
                        </div>

                        <div className="hidden md:flex items-center gap-8">
                            <button onClick={() => scrollToSection('features')} className="text-gray-700 hover:text-[#6C63FF] font-medium transition-colors">
                                Features
                            </button>
                            <button onClick={() => scrollToSection('how-it-works')} className="text-gray-700 hover:text-[#6C63FF] font-medium transition-colors">
                                How It Works
                            </button>
                            <button onClick={() => scrollToSection('departments')} className="text-gray-700 hover:text-[#6C63FF] font-medium transition-colors">
                                Departments
                            </button>
                            <button
                                onClick={() => navigate('/login')}
                                style={{
                                    padding: '10px 24px',
                                    background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                    color: 'white',
                                    borderRadius: '10px',
                                    fontWeight: '600',
                                    border: 'none',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease',
                                    boxShadow: '0 4px 12px rgba(108,99,255,0.3)'
                                }}
                                onMouseOver={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 6px 20px rgba(108,99,255,0.4)';
                                }}
                                onMouseOut={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(108,99,255,0.3)';
                                }}
                            >
                                Sign In
                            </button>
                        </div>

                        <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="md:hidden">
                            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>

                    {mobileMenuOpen && (
                        <div className="md:hidden mt-4 pb-4 space-y-3">
                            <button onClick={() => scrollToSection('features')} className="block w-full text-left py-2 text-gray-700">Features</button>
                            <button onClick={() => scrollToSection('how-it-works')} className="block w-full text-left py-2 text-gray-700">How It Works</button>
                            <button onClick={() => scrollToSection('departments')} className="block w-full text-left py-2 text-gray-700">Departments</button>
                            <button onClick={() => navigate('/login')} className="block w-full text-left py-2 text-[#6C63FF] font-medium">Sign In</button>
                        </div>
                    )}
                </div>
            </nav>

            {/* Hero Section */}
            <section style={{ paddingTop: '140px', paddingBottom: '100px', position: 'relative', overflow: 'hidden' }}>
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid md:grid-cols-2 gap-16 items-center">
                        <div>
                            <div style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '8px',
                                padding: '8px 18px',
                                background: 'linear-gradient(135deg, rgba(108,99,255,0.1) 0%, rgba(122,90,248,0.1) 100%)',
                                borderRadius: '24px',
                                marginBottom: '24px',
                                border: '1px solid rgba(108,99,255,0.2)'
                            }}>
                                <Zap size={16} style={{ color: '#6C63FF' }} />
                                <span style={{ color: '#6C63FF', fontWeight: '600', fontSize: '0.9rem' }}>
                                    Powered by Enterprise-Grade AI
                                </span>
                            </div>

                            <h1 style={{
                                fontSize: 'clamp(2.5rem, 5vw, 4.5rem)',
                                fontWeight: '800',
                                lineHeight: '1.1',
                                marginBottom: '24px',
                                color: '#1a1a2e'
                            }}>
                                Your Enterprise Knowledge,
                                <span style={{
                                    display: 'block',
                                    background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent',
                                    marginTop: '8px'
                                }}>
                                    Powered by AI
                                </span>
                            </h1>

                            <p style={{
                                fontSize: '1.25rem',
                                color: '#64748b',
                                marginBottom: '32px',
                                lineHeight: '1.8'
                            }}>
                                Instant, accurate answers from your company documents using advanced RAG technology.
                            </p>

                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginBottom: '40px' }}>
                                <button
                                    onClick={() => navigate('/login')}
                                    style={{
                                        padding: '16px 32px',
                                        background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                        color: 'white',
                                        borderRadius: '12px',
                                        fontWeight: '600',
                                        fontSize: '1.1rem',
                                        border: 'none',
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease',
                                        boxShadow: '0 8px 24px rgba(108,99,255,0.3)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px'
                                    }}
                                    onMouseOver={(e) => {
                                        e.currentTarget.style.transform = 'translateY(-4px)';
                                        e.currentTarget.style.boxShadow = '0 12px 32px rgba(108,99,255,0.4)';
                                    }}
                                    onMouseOut={(e) => {
                                        e.currentTarget.style.transform = 'translateY(0)';
                                        e.currentTarget.style.boxShadow = '0 8px 24px rgba(108,99,255,0.3)';
                                    }}
                                >
                                    Get Started Free <ArrowRight size={20} />
                                </button>

                                <button
                                    onClick={() => scrollToSection('demo')}
                                    style={{
                                        padding: '16px 32px',
                                        background: 'white',
                                        color: '#6C63FF',
                                        borderRadius: '12px',
                                        fontWeight: '600',
                                        fontSize: '1.1rem',
                                        border: '2px solid #6C63FF',
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px'
                                    }}
                                    onMouseOver={(e) => {
                                        e.currentTarget.style.background = '#6C63FF';
                                        e.currentTarget.style.color = 'white';
                                    }}
                                    onMouseOut={(e) => {
                                        e.currentTarget.style.background = 'white';
                                        e.currentTarget.style.color = '#6C63FF';
                                    }}
                                >
                                    <Play size={20} /> Watch Demo
                                </button>
                            </div>

                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '24px' }}>
                                {[
                                    { icon: CheckCircle, text: 'No credit card required' },
                                    { icon: CheckCircle, text: 'Setup in 5 minutes' },
                                    { icon: CheckCircle, text: 'Enterprise secure' }
                                ].map((item, i) => (
                                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <item.icon size={20} style={{ color: '#10b981' }} />
                                        <span style={{ color: '#64748b', fontSize: '0.95rem' }}>{item.text}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Animated Mockup */}
                        <div style={{ position: 'relative' }}>
                            <div style={{
                                background: 'white',
                                borderRadius: '24px',
                                boxShadow: '0 20px 60px rgba(108,99,255,0.15)',
                                padding: '24px',
                                border: '1px solid rgba(108,99,255,0.1)'
                            }}>
                                <div style={{
                                    background: 'linear-gradient(135deg, #F8F7FF 0%, #ECEBFF 100%)',
                                    borderRadius: '16px',
                                    padding: '24px',
                                    minHeight: '400px'
                                }}>
                                    <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px' }}>
                                        <div style={{
                                            background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                            color: 'white',
                                            padding: '12px 20px',
                                            borderRadius: '16px 16px 4px 16px',
                                            maxWidth: '80%',
                                            boxShadow: '0 4px 12px rgba(108,99,255,0.3)'
                                        }}>
                                            What is the annual leave policy?
                                        </div>
                                    </div>

                                    <div style={{ display: 'flex', gap: '12px' }}>
                                        <div style={{
                                            width: '40px',
                                            height: '40px',
                                            borderRadius: '50%',
                                            background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            flexShrink: 0
                                        }}>
                                            <Sparkles size={20} style={{ color: 'white' }} />
                                        </div>
                                        <div style={{
                                            background: 'white',
                                            padding: '16px 20px',
                                            borderRadius: '16px 16px 16px 4px',
                                            flex: 1,
                                            boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                                        }}>
                                            <p style={{ fontSize: '0.95rem', color: '#1a1a2e', marginBottom: '12px', lineHeight: '1.6' }}>
                                                Based on our HR policy, employees are entitled to <strong>20 days of annual leave</strong> per year. This includes:
                                            </p>
                                            <ul style={{ fontSize: '0.9rem', color: '#64748b', marginLeft: '20px', marginBottom: '12px' }}>
                                                <li>15 days paid vacation</li>
                                                <li>5 days personal leave</li>
                                            </ul>
                                            <div style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '6px',
                                                fontSize: '0.85rem',
                                                color: '#6C63FF',
                                                fontWeight: '500',
                                                marginTop: '12px',
                                                padding: '8px 12px',
                                                background: 'rgba(108,99,255,0.05)',
                                                borderRadius: '8px',
                                                width: 'fit-content'
                                            }}>
                                                <Link2 size={14} />
                                                📎 Source: HR_Policy.pdf
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Floating Badges */}
                            <div style={{
                                position: 'absolute',
                                top: '-20px',
                                right: '-20px',
                                background: 'white',
                                borderRadius: '16px',
                                padding: '12px 20px',
                                boxShadow: '0 8px 24px rgba(108,99,255,0.2)',
                                animation: 'float 3s ease-in-out infinite',
                                border: '1px solid rgba(108,99,255,0.1)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <Zap size={18} style={{ color: '#fbbf24' }} />
                                    <span style={{ fontWeight: '600', fontSize: '0.9rem', color: '#1a1a2e' }}>
                                        Instant Answers
                                    </span>
                                </div>
                            </div>

                            <div style={{
                                position: 'absolute',
                                bottom: '-20px',
                                left: '-20px',
                                background: 'white',
                                borderRadius: '16px',
                                padding: '12px 20px',
                                boxShadow: '0 8px 24px rgba(108,99,255,0.2)',
                                animation: 'float 3s ease-in-out infinite 1.5s',
                                border: '1px solid rgba(108,99,255,0.1)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <Shield size={18} style={{ color: '#10b981' }} />
                                    <span style={{ fontWeight: '600', fontSize: '0.9rem', color: '#1a1a2e' }}>
                                        100% Secure
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style={{
                    position: 'absolute',
                    bottom: '40px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    animation: 'bounce 2s ease-in-out infinite'
                }}>
                    <ChevronDown size={32} style={{ color: '#6C63FF' }} />
                </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works" style={{ padding: '100px 24px', background: 'white' }}>
                <div className="max-w-7xl mx-auto">
                    <div style={{ textAlign: 'center', marginBottom: '80px' }}>
                        <h2 style={{
                            fontSize: 'clamp(2rem, 4vw, 3.5rem)',
                            fontWeight: '800',
                            color: '#1a1a2e',
                            marginBottom: '16px'
                        }}>
                            How It Works in 3 Simple Steps
                        </h2>
                        <p style={{ fontSize: '1.2rem', color: '#64748b' }}>
                            Get started in minutes — no technical setup required
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-12">
                        {[
                            {
                                icon: Upload,
                                number: '1',
                                title: 'Upload Documents',
                                description: 'Add any PDF, DOCX, or TXT file. Department admins can upload internal documents securely.',
                                gradient: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)'
                            },
                            {
                                icon: MessageSquare,
                                number: '2',
                                title: 'Ask Questions',
                                description: 'Employees ask anything related to HR, Finance, Engineering, Policies, or Operations.',
                                gradient: 'linear-gradient(135deg, #7A5AF8 0%, #9D50BB 100%)'
                            },
                            {
                                icon: Sparkles,
                                number: '3',
                                title: 'Get Instant Answers',
                                description: 'AI finds the most relevant information and answers with accuracy + source citations.',
                                gradient: 'linear-gradient(135deg, #9D50BB 0%, #6C63FF 100%)'
                            }
                        ].map((step, i) => (
                            <div key={i} style={{ textAlign: 'center', position: 'relative' }}>
                                <div style={{
                                    width: '140px',
                                    height: '140px',
                                    background: step.gradient,
                                    borderRadius: '28px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    margin: '0 auto 32px',
                                    boxShadow: '0 12px 32px rgba(108,99,255,0.3)',
                                    transition: 'all 0.3s ease',
                                    cursor: 'pointer',
                                    position: 'relative'
                                }}
                                    onMouseOver={(e) => {
                                        e.currentTarget.style.transform = 'translateY(-8px) rotate(3deg)';
                                        e.currentTarget.style.boxShadow = '0 16px 40px rgba(108,99,255,0.4)';
                                    }}
                                    onMouseOut={(e) => {
                                        e.currentTarget.style.transform = 'translateY(0) rotate(0deg)';
                                        e.currentTarget.style.boxShadow = '0 12px 32px rgba(108,99,255,0.3)';
                                    }}
                                >
                                    <step.icon size={56} style={{ color: 'white' }} />
                                    <div style={{
                                        position: 'absolute',
                                        top: '-12px',
                                        right: '-12px',
                                        width: '36px',
                                        height: '36px',
                                        background: 'white',
                                        borderRadius: '50%',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontWeight: '800',
                                        fontSize: '1.2rem',
                                        color: '#6C63FF',
                                        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                                    }}>
                                        {step.number}
                                    </div>
                                </div>
                                <h3 style={{
                                    fontSize: '1.75rem',
                                    fontWeight: '700',
                                    color: '#1a1a2e',
                                    marginBottom: '16px'
                                }}>
                                    {step.title}
                                </h3>
                                <p style={{
                                    fontSize: '1.1rem',
                                    color: '#64748b',
                                    lineHeight: '1.7'
                                }}>
                                    {step.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" style={{
                padding: '100px 24px',
                background: 'linear-gradient(180deg, #F8F7FF 0%, white 100%)'
            }}>
                <div className="max-w-7xl mx-auto">
                    <div style={{ textAlign: 'center', marginBottom: '80px' }}>
                        <h2 style={{
                            fontSize: 'clamp(2rem, 4vw, 3.5rem)',
                            fontWeight: '800',
                            color: '#1a1a2e',
                            marginBottom: '16px'
                        }}>
                            Features That We Offer
                        </h2>
                        <p style={{ fontSize: '1.2rem', color: '#64748b' }}>
                            Everything you need for intelligent knowledge management
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {[
                            {
                                icon: Brain,
                                title: 'AI-Powered Search',
                                description: 'Advanced RAG retrieval for enterprise accuracy',
                                color: '#6C63FF'
                            },
                            {
                                icon: FileText,
                                title: 'Smart Document Processing',
                                description: 'Automatically processes, chunks, and indexes documents',
                                color: '#7A5AF8'
                            },
                            {
                                icon: Link2,
                                title: 'Source Citations',
                                description: 'Every answer includes verified references',
                                color: '#9D50BB'
                            },
                            {
                                icon: Shield,
                                title: 'Role-Based Access',
                                description: 'Admins, HR, Finance, Engineering, Employee dashboards',
                                color: '#10b981'
                            },
                            {
                                icon: Users,
                                title: 'Secure Data Storage',
                                description: 'Document files and employee profiles stored securely',
                                color: '#3b82f6'
                            },
                            {
                                icon: Zap,
                                title: 'Lightning-Fast Responses',
                                description: 'LLM answers within 2 seconds using optimized context',
                                color: '#f59e0b'
                            }
                        ].map((feature, i) => (
                            <div
                                key={i}
                                style={{
                                    background: 'white',
                                    padding: '40px',
                                    borderRadius: '24px',
                                    border: '1px solid rgba(108,99,255,0.1)',
                                    transition: 'all 0.3s ease',
                                    cursor: 'pointer'
                                }}
                                onMouseOver={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-8px)';
                                    e.currentTarget.style.boxShadow = '0 20px 40px rgba(108,99,255,0.15)';
                                    e.currentTarget.style.borderColor = feature.color;
                                }}
                                onMouseOut={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = 'none';
                                    e.currentTarget.style.borderColor = 'rgba(108,99,255,0.1)';
                                }}
                            >
                                <div style={{
                                    width: '72px',
                                    height: '72px',
                                    background: `${feature.color}15`,
                                    borderRadius: '18px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    marginBottom: '24px'
                                }}>
                                    <feature.icon size={36} style={{ color: feature.color }} />
                                </div>
                                <h3 style={{
                                    fontSize: '1.5rem',
                                    fontWeight: '700',
                                    color: '#1a1a2e',
                                    marginBottom: '12px'
                                }}>
                                    {feature.title}
                                </h3>
                                <p style={{
                                    fontSize: '1rem',
                                    color: '#64748b',
                                    lineHeight: '1.7'
                                }}>
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Departments Section */}
            <section id="departments" style={{ padding: '100px 24px', background: 'white' }}>
                <div className="max-w-7xl mx-auto">
                    <div style={{ textAlign: 'center', marginBottom: '80px' }}>
                        <h2 style={{
                            fontSize: 'clamp(2rem, 4vw, 3.5rem)',
                            fontWeight: '800',
                            color: '#1a1a2e',
                            marginBottom: '16px'
                        }}>
                            Built for Every Department
                        </h2>
                        <p style={{ fontSize: '1.2rem', color: '#64748b', marginBottom: '12px' }}>
                            Tailored solutions for your entire organization
                        </p>
                        <p style={{
                            fontSize: '1.1rem',
                            color: '#6C63FF',
                            fontWeight: '600',
                            fontStyle: 'italic'
                        }}>
                            "Each user sees answers only from the documents allowed for their role"
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {[
                            { icon: Users, name: 'HR', desc: 'Policies, leave, payroll', color: '#E91E63' },
                            { icon: DollarSign, name: 'Finance', desc: 'Budget rules, approvals', color: '#4CAF50' },
                            { icon: Code, name: 'Engineering', desc: 'Technical docs, SOPs', color: '#2196F3' },
                            { icon: Settings, name: 'Operations', desc: 'Processes, workflows', color: '#FF9800' },
                            { icon: Building2, name: 'Admin', desc: 'User creation, docs', color: '#607D8B' },
                            { icon: Users, name: 'Sales', desc: 'Proposals, contracts', color: '#9C27B0' },
                            { icon: MessageSquare, name: 'Marketing', desc: 'Campaigns, content', color: '#FF5722' },
                            { icon: Shield, name: 'Legal', desc: 'Compliance, contracts', color: '#795548' }
                        ].map((dept, i) => (
                            <div
                                key={i}
                                style={{
                                    background: `linear-gradient(135deg, ${dept.color}10 0%, ${dept.color}05 100%)`,
                                    padding: '32px',
                                    borderRadius: '20px',
                                    border: `2px solid ${dept.color}20`,
                                    transition: 'all 0.3s ease',
                                    cursor: 'pointer',
                                    textAlign: 'center'
                                }}
                                onMouseOver={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-8px)';
                                    e.currentTarget.style.borderColor = dept.color;
                                    e.currentTarget.style.boxShadow = `0 12px 32px ${dept.color}30`;
                                }}
                                onMouseOut={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.borderColor = `${dept.color}20`;
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                <div style={{
                                    width: '64px',
                                    height: '64px',
                                    background: dept.color,
                                    borderRadius: '16px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    margin: '0 auto 16px'
                                }}>
                                    <dept.icon size={32} style={{ color: 'white' }} />
                                </div>
                                <h3 style={{
                                    fontSize: '1.25rem',
                                    fontWeight: '700',
                                    color: '#1a1a2e',
                                    marginBottom: '8px'
                                }}>
                                    {dept.name}
                                </h3>
                                <p style={{ fontSize: '0.95rem', color: '#64748b' }}>
                                    {dept.desc}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* User Profile Management Section */}
            <section style={{
                padding: '100px 24px',
                background: 'linear-gradient(180deg, #F8F7FF 0%, #ECEBFF 100%)'
            }}>
                <div className="max-w-5xl mx-auto">
                    <div className="grid md:grid-cols-2 gap-16 items-center">
                        <div>
                            <h2 style={{
                                fontSize: 'clamp(2rem, 4vw, 3rem)',
                                fontWeight: '800',
                                color: '#1a1a2e',
                                marginBottom: '24px'
                            }}>
                                Complete User Profile Management
                            </h2>
                            <p style={{
                                fontSize: '1.15rem',
                                color: '#64748b',
                                lineHeight: '1.8',
                                marginBottom: '24px'
                            }}>
                                Employees can update their photo, name, and contact details. Changes apply instantly across the platform.
                            </p>
                            <ul style={{ fontSize: '1.05rem', color: '#64748b', lineHeight: '2' }}>
                                <li>✓ Upload and update profile photos</li>
                                <li>✓ Edit personal information</li>
                                <li>✓ Update contact details</li>
                                <li>✓ Secure data storage in database</li>
                            </ul>
                        </div>

                        <div style={{
                            background: 'white',
                            borderRadius: '24px',
                            padding: '32px',
                            boxShadow: '0 20px 60px rgba(108,99,255,0.15)',
                            border: '1px solid rgba(108,99,255,0.1)'
                        }}>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '16px',
                                marginBottom: '24px',
                                padding: '16px',
                                background: 'linear-gradient(135deg, #F8F7FF 0%, #ECEBFF 100%)',
                                borderRadius: '16px'
                            }}>
                                <div style={{
                                    width: '64px',
                                    height: '64px',
                                    borderRadius: '50%',
                                    background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'white',
                                    fontSize: '1.5rem',
                                    fontWeight: '700'
                                }}>
                                    JD
                                </div>
                                <div>
                                    <h4 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#1a1a2e' }}>John Doe</h4>
                                    <p style={{ fontSize: '0.9rem', color: '#64748b' }}>john.doe@company.com</p>
                                </div>
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {[
                                    { icon: Upload, text: 'Update Photo' },
                                    { icon: Users, text: 'Update Name' },
                                    { icon: MessageSquare, text: 'Update Email' },
                                    { icon: Shield, text: 'Logout' }
                                ].map((item, i) => (
                                    <div
                                        key={i}
                                        style={{
                                            padding: '14px 18px',
                                            background: '#F8F7FF',
                                            borderRadius: '12px',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '12px',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease',
                                            border: '1px solid transparent'
                                        }}
                                        onMouseOver={(e) => {
                                            e.currentTarget.style.background = 'white';
                                            e.currentTarget.style.borderColor = '#6C63FF';
                                        }}
                                        onMouseOut={(e) => {
                                            e.currentTarget.style.background = '#F8F7FF';
                                            e.currentTarget.style.borderColor = 'transparent';
                                        }}
                                    >
                                        <item.icon size={20} style={{ color: '#6C63FF' }} />
                                        <span style={{ fontWeight: '500', color: '#1a1a2e' }}>{item.text}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Demo Preview Section */}
            <section id="demo" style={{ padding: '100px 24px', background: 'white' }}>
                <div className="max-w-6xl mx-auto">
                    <div style={{ textAlign: 'center', marginBottom: '60px' }}>
                        <h2 style={{
                            fontSize: 'clamp(2rem, 4vw, 3.5rem)',
                            fontWeight: '800',
                            color: '#1a1a2e',
                            marginBottom: '16px'
                        }}>
                            Try the AI Assistant
                        </h2>
                        <p style={{ fontSize: '1.2rem', color: '#64748b' }}>
                            See how easy it is to get instant answers
                        </p>
                    </div>

                    <div style={{
                        background: 'linear-gradient(135deg, #F8F7FF 0%, #ECEBFF 100%)',
                        borderRadius: '28px',
                        padding: '48px',
                        border: '2px solid rgba(108,99,255,0.2)'
                    }}>
                        <div style={{
                            background: 'white',
                            borderRadius: '20px',
                            padding: '32px',
                            marginBottom: '32px',
                            boxShadow: '0 8px 24px rgba(0,0,0,0.05)'
                        }}>
                            <h3 style={{
                                fontSize: '1.3rem',
                                fontWeight: '700',
                                color: '#1a1a2e',
                                marginBottom: '20px'
                            }}>
                                Try asking:
                            </h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {[
                                    'Show me the HR holiday rules.',
                                    'What is the expense reimbursement process?',
                                    'Explain the onboarding steps.'
                                ].map((question, i) => (
                                    <div
                                        key={i}
                                        style={{
                                            padding: '16px 20px',
                                            background: activeDemo === i ? 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)' : '#F8F7FF',
                                            color: activeDemo === i ? 'white' : '#1a1a2e',
                                            borderRadius: '12px',
                                            cursor: 'pointer',
                                            transition: 'all 0.3s ease',
                                            fontWeight: '500',
                                            border: activeDemo === i ? 'none' : '1px solid rgba(108,99,255,0.2)'
                                        }}
                                        onClick={() => setActiveDemo(i)}
                                        onMouseOver={(e) => {
                                            if (activeDemo !== i) {
                                                e.currentTarget.style.background = 'white';
                                                e.currentTarget.style.borderColor = '#6C63FF';
                                            }
                                        }}
                                        onMouseOut={(e) => {
                                            if (activeDemo !== i) {
                                                e.currentTarget.style.background = '#F8F7FF';
                                                e.currentTarget.style.borderColor = 'rgba(108,99,255,0.2)';
                                            }
                                        }}
                                    >
                                        {question}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div style={{
                            background: 'white',
                            borderRadius: '20px',
                            padding: '32px',
                            boxShadow: '0 8px 24px rgba(0,0,0,0.05)'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
                                <div style={{
                                    width: '40px',
                                    height: '40px',
                                    borderRadius: '50%',
                                    background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}>
                                    <Sparkles size={20} style={{ color: 'white' }} />
                                </div>
                                <div>
                                    <h4 style={{ fontWeight: '700', color: '#1a1a2e' }}>AI Assistant</h4>
                                    <p style={{ fontSize: '0.85rem', color: '#64748b' }}>Powered by RAG Technology</p>
                                </div>
                            </div>
                            <p style={{
                                fontSize: '1.05rem',
                                color: '#1a1a2e',
                                lineHeight: '1.7',
                                marginBottom: '16px'
                            }}>
                                {activeDemo === 0 && 'According to our HR policy, employees receive 10 public holidays, 15 vacation days, and 5 personal days per year. Holiday schedules are published quarterly.'}
                                {activeDemo === 1 && 'To request expense reimbursement: 1) Submit receipts via the Finance Portal, 2) Fill out the expense form, 3) Get manager approval. Processing takes 5-7 business days.'}
                                {activeDemo === 2 && 'New employee onboarding includes: Day 1 - IT setup & orientation, Week 1 - Department training, Week 2 - Role-specific training, Month 1 - Performance check-in with manager.'}
                            </p>
                            <div style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '6px',
                                fontSize: '0.85rem',
                                color: '#6C63FF',
                                fontWeight: '500',
                                padding: '8px 14px',
                                background: 'rgba(108,99,255,0.05)',
                                borderRadius: '8px'
                            }}>
                                <Link2 size={14} />
                                📎 Source: {activeDemo === 0 ? 'HR_Policy.pdf' : activeDemo === 1 ? 'Finance_Guidelines.pdf' : 'Onboarding_Guide.pdf'}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section style={{
                padding: '120px 24px',
                background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div className="max-w-4xl mx-auto" style={{ textAlign: 'center', position: 'relative', zIndex: 1 }}>
                    <h2 style={{
                        fontSize: 'clamp(2.5rem, 5vw, 4rem)',
                        fontWeight: '800',
                        color: 'white',
                        marginBottom: '24px',
                        lineHeight: '1.2'
                    }}>
                        Start Using AI in Your Company Today
                    </h2>
                    <p style={{
                        fontSize: '1.3rem',
                        color: 'rgba(255,255,255,0.9)',
                        marginBottom: '48px',
                        lineHeight: '1.6'
                    }}>
                        Get instant, accurate answers. Empower every employee.
                    </p>

                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
                        <button
                            onClick={() => navigate('/login')}
                            style={{
                                padding: '18px 40px',
                                background: 'white',
                                color: '#6C63FF',
                                borderRadius: '12px',
                                fontWeight: '700',
                                fontSize: '1.15rem',
                                border: 'none',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease',
                                boxShadow: '0 8px 24px rgba(0,0,0,0.15)'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.transform = 'translateY(-4px)';
                                e.currentTarget.style.boxShadow = '0 12px 32px rgba(0,0,0,0.2)';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.15)';
                            }}
                        >
                            Start Now →
                        </button>

                        <button
                            onClick={() => scrollToSection('demo')}
                            style={{
                                padding: '18px 40px',
                                background: 'transparent',
                                color: 'white',
                                borderRadius: '12px',
                                fontWeight: '700',
                                fontSize: '1.15rem',
                                border: '2px solid white',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
                                e.currentTarget.style.transform = 'translateY(-4px)';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.transform = 'translateY(0)';
                            }}
                        >
                            Request a Demo
                        </button>
                    </div>
                </div>

                <div style={{
                    position: 'absolute',
                    top: '10%',
                    left: '5%',
                    width: '400px',
                    height: '400px',
                    background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
                    borderRadius: '50%',
                    animation: 'float 8s ease-in-out infinite'
                }}></div>
                <div style={{
                    position: 'absolute',
                    bottom: '10%',
                    right: '5%',
                    width: '300px',
                    height: '300px',
                    background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
                    borderRadius: '50%',
                    animation: 'float 10s ease-in-out infinite reverse'
                }}></div>
            </section>

            {/* Footer */}
            <footer style={{
                padding: '60px 24px 40px',
                background: '#1a1a2e',
                color: 'white'
            }}>
                <div className="max-w-7xl mx-auto">
                    <div className="grid md:grid-cols-4 gap-12 mb-12">
                        <div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                                <div style={{
                                    width: '40px',
                                    height: '40px',
                                    background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                                    borderRadius: '10px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}>
                                    <Sparkles size={20} style={{ color: 'white' }} />
                                </div>
                                <span style={{ fontSize: '1.2rem', fontWeight: '700' }}>AI Enterprise RAG</span>
                            </div>
                            <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.95rem', lineHeight: '1.6' }}>
                                Your enterprise knowledge, powered by AI. Get instant, accurate answers from your documents.
                            </p>
                        </div>

                        <div>
                            <h4 style={{ fontWeight: '700', marginBottom: '16px' }}>Product</h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                <a href="#features" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>Features</a>
                                <a href="#how-it-works" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>How It Works</a>
                                <a href="#departments" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>Departments</a>
                            </div>
                        </div>

                        <div>
                            <h4 style={{ fontWeight: '700', marginBottom: '16px' }}>Company</h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                <a href="#" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>About Us</a>
                                <a href="#" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>Privacy Policy</a>
                                <a href="#" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>Terms of Service</a>
                            </div>
                        </div>

                        <div>
                            <h4 style={{ fontWeight: '700', marginBottom: '16px' }}>Contact</h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                <a href="mailto:support@enterprise-rag.com" style={{ color: 'rgba(255,255,255,0.7)', textDecoration: 'none', fontSize: '0.95rem' }}>
                                    support@enterprise-rag.com
                                </a>
                                <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.95rem' }}>
                                    Available 24/7
                                </p>
                            </div>
                        </div>
                    </div>

                    <div style={{ marginTop: '32px', display: 'flex', gap: '16px' }}>
                        <a href="https://www.linkedin.com/in/mahesh-k-6a4520291/" target="_blank" rel="noopener noreferrer" style={{
                            width: '40px',
                            height: '40px',
                            background: 'rgba(255,255,255,0.1)',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            transition: 'all 0.3s ease'
                        }}
                            onMouseOver={(e) => e.currentTarget.style.background = '#0077b5'}
                            onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.1)'}
                        >
                            <Linkedin size={20} />
                        </a>
                    </div>

                    <div style={{
                        paddingTop: '32px',
                        borderTop: '1px solid rgba(255,255,255,0.1)',
                        textAlign: 'center',
                        color: 'rgba(255,255,255,0.5)',
                        fontSize: '0.9rem'
                    }}>
                        © 2024 AI Enterprise RAG Assistant. All rights reserved.
                    </div>
                </div>
            </footer>

            <style>{`
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-20px); }
                }

                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }

                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            `}</style>
        </div>
    );
}

export default LandingPage;
