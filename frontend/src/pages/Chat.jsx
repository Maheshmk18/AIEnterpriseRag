import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Send, Plus, MessageSquare, Trash2, LogOut,
  User, ChevronDown, Sparkles, Home
} from 'lucide-react';
import api from '../services/api';
import { getUser } from '../utils/auth';
import ProfileModal from '../components/ProfileModal';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Role-specific suggested questions
const ROLE_QUESTIONS = {
  admin: {
    title: 'AI Assistant',
    description: 'Full access to all company documents and knowledge base.',
    questions: [
      'What documents are in the knowledge base?',
      'Show me all company policies',
      'What are the latest updates?',
      'Company overview and structure?',
      'All department guidelines?',
      'System administration info?'
    ]
  },
  hr: {
    title: 'AI Assistant',
    description: 'Ask about HR policies, employee management, and benefits.',
    questions: [
      'What is the annual leave policy?',
      'How do I apply for sick leave?',
      'What is the onboarding process?',
      'Employee benefits overview?',
      'How does the performance review work?',
      'What is the maternity/paternity leave policy?'
    ]
  },
  manager: {
    title: 'AI Assistant',
    description: 'Ask about management policies, team operations, and leadership.',
    questions: [
      'Team management best practices?',
      'Performance review guidelines?',
      'Budget approval process?',
      'How to handle team conflicts?',
      'Hiring and recruitment process?',
      'Employee development programs?'
    ]
  },
  employee: {
    title: 'AI Assistant',
    description: 'Ask about general company policies and information.',
    questions: [
      'What is the work from home policy?',
      'Office timings and holidays?',
      'How do I submit an expense report?',
      'Company values and mission?',
      'Employee code of conduct?',
      'Training and development?'
    ]
  }
};

function Chat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [user, setUser] = useState(null);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setUser(getUser());
    fetchSessions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchSessions = async () => {
    try {
      const response = await api.get('/chat/sessions');
      setSessions(response.data || []);
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    }
  };

  const loadSession = async (sessionId) => {
    try {
      const response = await api.get(`/chat/sessions/${sessionId}`);
      setCurrentSession(sessionId);
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error('Failed to load session:', error);
    }
  };

  const handleNewChat = () => {
    setCurrentSession(null);
    setMessages([]);
  };

  // Streaming Chat Handler
  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    // Assistant placeholder will be added when the first token arrives

    try {
      const token = localStorage.getItem('token');
      // Ensure we use the correct API URL regardless of how it's defined
      const baseUrl = import.meta.env.VITE_API_URL || '/api/v1';
      const url = `${baseUrl}/chat/stream`.replace(/\/\//g, '/').replace(':/', '://');

      console.log('Fetching stream from:', url);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: currentSession
        })
      });

      console.log('Stream response status:', response.status);

      if (!response.ok) {
        let errorMsg = `Server error: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || errorMsg;
        } catch (e) {
          const errorText = await response.text();
          errorMsg = errorText || errorMsg;
        }
        throw new Error(errorMsg);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantResponse = "";
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          console.log('Stream finished.');
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        // Split by standard SSE double newline
        const lines = buffer.split('\n\n');
        // The last element might be a partial line, keep it in the buffer
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine) continue;

          if (trimmedLine.startsWith('data: ')) {
            try {
              const dataText = trimmedLine.substring(6);
              if (dataText === '[DONE]') break;

              const data = JSON.parse(dataText);

              if (data.error) {
                console.error('AI Error:', data.error);
                assistantResponse = `**Error:** ${data.error}`;
                updateLastMessage(assistantResponse);
                continue;
              }

              if (data.content) {
                assistantResponse += data.content;
                updateLastMessage(assistantResponse);
              }

              if (data.done && data.session_id && !currentSession) {
                setCurrentSession(data.session_id);
                fetchSessions();
              }
            } catch (e) {
              console.warn('Failed to parse SSE line:', trimmedLine, e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      updateLastMessage(`I apologize, but I encountered an error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const updateLastMessage = (content) => {
    setMessages(prev => {
      const last = prev[prev.length - 1];
      if (last?.role === 'assistant') {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1] = { ...last, content };
        return newMsgs;
      } else {
        return [...prev, { role: 'assistant', content }];
      }
    });
  };

  const handleQuickQuestion = (question) => {
    setInput(question);
    setTimeout(() => {
      setMessages(prev => [...prev, { role: 'user', content: question }]);
      setInput('');
      setLoading(true);

      api.post('/chat/', {
        message: question,
        session_id: currentSession
      }).then(response => {
        const assistantResponse = response.data?.response || 'I received your message.';
        setMessages(prev => [...prev, { role: 'assistant', content: assistantResponse }]);
        if (!currentSession && response.data?.session_id) {
          setCurrentSession(response.data.session_id);
          fetchSessions();
        }
      }).catch(error => {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, an error occurred.' }]);
      }).finally(() => {
        setLoading(false);
      });
    }, 100);
  };

  const deleteSession = async (sessionId, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this chat session?')) return;

    try {
      console.log('Deleting session:', sessionId);
      const response = await api.delete(`/chat/sessions/${sessionId}`);
      console.log('Delete response:', response.data);

      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSession === sessionId) {
        handleNewChat();
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
      alert('Failed to delete session: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const getInitials = (name) => {
    return name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U';
  };

  const userRole = user?.role || 'employee';
  const roleConfig = ROLE_QUESTIONS[userRole] || ROLE_QUESTIONS.employee;

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#FAFAFA' }}>
      {/* Sidebar */}
      <div style={{
        width: '280px',
        height: '100vh',
        background: 'white',
        borderRight: '1px solid #E5E7EB',
        display: 'flex',
        flexDirection: 'column',
        position: 'fixed',
        left: 0,
        top: 0
      }}>
        {/* Logo Header */}
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid #E5E7EB'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <img src="/logo.png" alt="Logo" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
            </div>
            <div>
              <div style={{ fontWeight: '700', fontSize: '1rem', color: '#1F2937' }}>Enterprise RAG</div>
              <div style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>AI Assistant</div>
            </div>
          </div>
        </div>

        {/* New Chat Button */}
        <div style={{ padding: '16px' }}>
          <button
            onClick={handleNewChat}
            style={{
              width: '100%',
              padding: '12px 16px',
              background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
              color: 'white',
              borderRadius: '10px',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 12px rgba(108,99,255,0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
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
            <Plus size={18} />
            New Chat
          </button>
        </div>

        {/* Recent Chats */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '0 16px'
        }}>
          <div style={{
            fontSize: '0.75rem',
            color: '#9CA3AF',
            padding: '8px 12px',
            textTransform: 'uppercase',
            fontWeight: '600',
            letterSpacing: '0.05em'
          }}>
            RECENT CHATS
          </div>
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => loadSession(session.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                borderRadius: '10px',
                cursor: 'pointer',
                transition: 'all 0.2s',
                background: currentSession === session.id ? 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)' : 'transparent',
                color: currentSession === session.id ? 'white' : '#6B7280',
                marginBottom: '4px'
              }}
              onMouseOver={(e) => {
                if (currentSession !== session.id) {
                  e.currentTarget.style.background = '#F3F4F6';
                }
              }}
              onMouseOut={(e) => {
                if (currentSession !== session.id) {
                  e.currentTarget.style.background = 'transparent';
                }
              }}
            >
              <MessageSquare size={16} />
              <span style={{
                flex: 1,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
                fontWeight: currentSession === session.id ? '500' : '400'
              }}>
                {session.title}
              </span>
              <button
                onClick={(e) => deleteSession(session.id, e)}
                title="Delete Chat"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: currentSession === session.id ? 'white' : '#9CA3AF',
                  cursor: 'pointer',
                  padding: '8px',
                  opacity: 0.6,
                  display: 'flex',
                  alignItems: 'center',
                  transition: 'opacity 0.2s, transform 0.2s',
                  borderRadius: '6px'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.opacity = '1';
                  e.currentTarget.style.background = currentSession === session.id ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.05)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.opacity = '0.6';
                  e.currentTarget.style.background = 'transparent';
                }}
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>

        {/* Dashboard Button */}
        <div style={{ padding: '16px', borderTop: '1px solid #E5E7EB' }}>
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              width: '100%',
              padding: '12px 16px',
              background: 'white',
              color: '#6C63FF',
              borderRadius: '10px',
              fontWeight: '600',
              border: '2px solid #6C63FF',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
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
            <Home size={18} />
            Dashboard
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', marginLeft: '280px' }}>
        {/* Header */}
        <div style={{
          background: 'white',
          borderBottom: '1px solid #E5E7EB',
          padding: '16px 32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1F2937' }}>
              AI Assistant
            </h2>
          </div>

          {/* Profile Dropdown */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '8px 16px',
                background: '#F9FAFB',
                border: '1px solid #E5E7EB',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = 'white';
                e.currentTarget.style.borderColor = '#6C63FF';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = '#F9FAFB';
                e.currentTarget.style.borderColor = '#E5E7EB';
              }}
            >
              {user?.profile_photo ? (
                <img src={user.profile_photo} alt="" style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  objectFit: 'cover'
                }} />
              ) : (
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: '600',
                  fontSize: '0.875rem',
                  color: 'white'
                }}>
                  {getInitials(user?.full_name)}
                </div>
              )}
              <div style={{ textAlign: 'left' }}>
                <div style={{ fontWeight: '600', fontSize: '0.9rem', color: '#1F2937' }}>{user?.role || 'Admin'}</div>
                <div style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>{user?.role || 'admin'}</div>
              </div>
              <ChevronDown size={16} style={{ color: '#9CA3AF' }} />
            </button>

            {showProfileMenu && (
              <div style={{
                position: 'absolute',
                top: '100%',
                right: 0,
                marginTop: '8px',
                minWidth: '220px',
                background: 'white',
                border: '1px solid #E5E7EB',
                borderRadius: '12px',
                padding: '8px',
                boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
                zIndex: 100
              }}>
                <button
                  onClick={() => { setShowProfileModal(true); setShowProfileMenu(false); }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    color: '#6B7280',
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                    cursor: 'pointer',
                    border: 'none',
                    background: 'transparent',
                    width: '100%',
                    fontSize: '0.95rem'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#F3F4F6';
                    e.currentTarget.style.color = '#1F2937';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.color = '#6B7280';
                  }}
                >
                  <User size={18} />
                  Edit Profile
                </button>
                <button
                  onClick={() => { navigate('/dashboard'); setShowProfileMenu(false); }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    color: '#6B7280',
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                    cursor: 'pointer',
                    border: 'none',
                    background: 'transparent',
                    width: '100%',
                    fontSize: '0.95rem'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#F3F4F6';
                    e.currentTarget.style.color = '#1F2937';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.color = '#6B7280';
                  }}
                >
                  <Home size={18} />
                  Dashboard
                </button>
                <div style={{ borderTop: '1px solid #E5E7EB', margin: '8px 0' }} />
                <button
                  onClick={handleLogout}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    color: '#EF4444',
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                    cursor: 'pointer',
                    border: 'none',
                    background: 'transparent',
                    width: '100%',
                    fontSize: '0.95rem'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#FEF2F2';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = 'transparent';
                  }}
                >
                  <LogOut size={18} />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px 32px',
          background: '#FAFAFA'
        }}>
          {messages.length === 0 ? (
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              gap: '24px'
            }}>
              <div style={{
                width: '80px',
                height: '80px',
                marginBottom: '16px',
                animation: 'pulse 2s ease-in-out infinite',
                filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.2))'
              }}>
                <img
                  src="/logo.png"
                  alt="Logo"
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain'
                  }}
                />
              </div>
              <div style={{ textAlign: 'center', maxWidth: '500px' }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '8px', color: '#1F2937' }}>
                  Hello! What can I help you with?
                </h2>
                <p style={{ color: '#6B7280', fontSize: '1rem' }}>
                  {roleConfig.description}
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    gap: '12px',
                    marginBottom: '16px',
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
                  }}
                >
                  {msg.role === 'assistant' && (
                    <div style={{
                      width: '36px',
                      height: '36px',
                      flexShrink: 0
                    }}>
                      <img src="/logo.png" alt="AI" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                    </div>
                  )}
                  <div style={{
                    padding: '14px 18px',
                    borderRadius: msg.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                    background: msg.role === 'user'
                      ? 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)'
                      : 'white',
                    color: msg.role === 'user' ? 'white' : '#1F2937',
                    maxWidth: '70%',
                    lineHeight: '1.6',
                    boxShadow: msg.role === 'user'
                      ? '0 4px 12px rgba(108,99,255,0.3)'
                      : '0 2px 8px rgba(0,0,0,0.05)',
                    border: msg.role === 'assistant' ? '1px solid #E5E7EB' : 'none'
                  }}>
                    {msg.role === 'assistant' ? (
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          p: ({ node, ...props }) => <p style={{ margin: '0 0 8px 0', lastChild: { margin: 0 } }} {...props} />,
                          ul: ({ node, ...props }) => <ul style={{ margin: '0 0 8px 0', paddingLeft: '20px' }} {...props} />,
                          ol: ({ node, ...props }) => <ol style={{ margin: '0 0 8px 0', paddingLeft: '20px' }} {...props} />,
                          li: ({ node, ...props }) => <li style={{ marginBottom: '4px' }} {...props} />,
                          strong: ({ node, ...props }) => <strong style={{ fontWeight: '600' }} {...props} />
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    ) : (
                      msg.content
                    )}
                  </div>
                </div>
              ))}
              {loading && messages[messages.length - 1]?.role !== 'assistant' && (
                <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
                  <div style={{
                    width: '36px',
                    height: '36px',
                    flexShrink: 0
                  }}>
                    <img src="/logo.png" alt="AI" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                  </div>
                  <div style={{
                    padding: '14px 18px',
                    borderRadius: '16px 16px 16px 4px',
                    background: 'white',
                    border: '1px solid #E5E7EB',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                  }}>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      <span style={{
                        width: '8px',
                        height: '8px',
                        background: '#6C63FF',
                        borderRadius: '50%',
                        animation: 'bounce 1.4s ease-in-out infinite'
                      }}></span>
                      <span style={{
                        width: '8px',
                        height: '8px',
                        background: '#6C63FF',
                        borderRadius: '50%',
                        animation: 'bounce 1.4s ease-in-out infinite 0.16s'
                      }}></span>
                      <span style={{
                        width: '8px',
                        height: '8px',
                        background: '#6C63FF',
                        borderRadius: '50%',
                        animation: 'bounce 1.4s ease-in-out infinite 0.32s'
                      }}></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div style={{
          background: 'white',
          borderTop: '1px solid #E5E7EB',
          padding: '20px 32px'
        }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about company documents..."
              disabled={loading}
              style={{
                flex: 1,
                padding: '16px 20px',
                fontSize: '1rem',
                background: '#F9FAFB',
                border: '1px solid #E5E7EB',
                borderRadius: '12px',
                color: '#1F2937',
                outline: 'none',
                transition: 'all 0.2s'
              }}
              onFocus={(e) => {
                e.currentTarget.style.borderColor = '#6C63FF';
                e.currentTarget.style.boxShadow = '0 0 0 3px rgba(108,99,255,0.1)';
              }}
              onBlur={(e) => {
                e.currentTarget.style.borderColor = '#E5E7EB';
                e.currentTarget.style.boxShadow = 'none';
              }}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                background: input.trim() && !loading
                  ? 'linear-gradient(135deg, #6C63FF 0%, #7A5AF8 100%)'
                  : '#E5E7EB',
                border: 'none',
                cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                transition: 'all 0.3s',
                boxShadow: input.trim() && !loading ? '0 4px 12px rgba(108,99,255,0.3)' : 'none'
              }}
              onMouseOver={(e) => {
                if (input.trim() && !loading) {
                  e.currentTarget.style.transform = 'scale(1.05)';
                  e.currentTarget.style.boxShadow = '0 6px 20px rgba(108,99,255,0.4)';
                }
              }}
              onMouseOut={(e) => {
                if (input.trim() && !loading) {
                  e.currentTarget.style.transform = 'scale(1)';
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(108,99,255,0.3)';
                }
              }}
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>

      {/* Profile Modal */}
      {showProfileModal && (
        <ProfileModal
          user={user}
          onClose={() => setShowProfileModal(false)}
          onUpdate={(updated) => setUser(updated)}
        />
      )}

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
      `}</style>
    </div>
  );
}

export default Chat;
