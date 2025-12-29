import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import clsx from 'clsx';
import { sendChatMessage, checkBackendHealth, ChatRequest, ChatResponse, ChatError } from '../../services/chat-api';
import './ChatWidget.css';

// Define TypeScript interfaces
interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'bot';
  timestamp: Date;
}

const ChatWidget: React.FC = () => {
  // State management
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      content: 'Welcome to the Physical AI & Humanoid Robotics textbook assistant. How can I help you today?',
      role: 'bot',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string>('');
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedText, setSelectedText] = useState<string>('');
  const [backendStatus, setBackendStatus] = useState<'checking' | 'ok' | 'error'>('checking');

  // Ref for auto-scrolling to bottom
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Check backend status on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const isHealthy = await checkBackendHealth();
        setBackendStatus(isHealthy ? 'ok' : 'error');

        if (!isHealthy) {
          // Add a system message to inform the user about backend status
          const statusMessage: ChatMessage = {
            id: `status-${Date.now()}`,
            content: '⚠️ Backend service may be unavailable. Some features might not work properly.',
            role: 'bot',
            timestamp: new Date(),
          };
          setMessages(prev => [...prev, statusMessage]);
        }
      } catch (err) {
        setBackendStatus('error');
        console.error('Backend health check failed:', err);
      }
    };

    checkBackend();
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '') {
        const selectedText = selection.toString();
        if (selectedText.length > 0 && selectedText.length < 500) { // Limit to reasonable selection size
          setSelectedText(selectedText);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to send message to backend
  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue;
    if (!textToSend.trim() || isLoading) return;

    try {
      // Clear any previous errors
      setError(null);

      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        content: textToSend,
        role: 'user',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage]);

      // Clear input field if not triggered by text selection
      if (!messageText) {
        setInputValue('');
      }

      // Clear selected text after sending
      if (messageText) {
        setSelectedText('');
      }

      // Set loading state
      setIsLoading(true);

      // Prepare the API request
      const requestBody: ChatRequest = {
        message: textToSend,
        session_id: sessionId || undefined, // Send session_id if we have one, otherwise let backend generate
      };

      const data: ChatResponse = await sendChatMessage(requestBody);

      // Update session ID if we got a new one
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      // Add bot response to messages
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        content: data.response,
        role: 'bot',
        timestamp: new Date(data.timestamp),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      const errorMessageText = err instanceof Error ? err.message : 'Connection Failed';

      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        content: errorMessageText,
        role: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      // Reset loading state
      setIsLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage();
  };

  // Handle selected text click (send selected text to chat)
  const handleSelectedTextClick = () => {
    if (selectedText) {
      sendMessage(selectedText);
    }
  };

  // Toggle chat window open/close
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Close chat window
  const closeChat = () => {
    setIsOpen(false);
  };

  // If chat is closed, show only the floating button
  if (!isOpen) {
    return (
      <div className="chat-fab" onClick={toggleChat} role="button" aria-label="Open chat">
        <div className="chat-icon">🤖</div>
      </div>
    );
  }

  // If chat is open, show the full chat widget
  return (
    <div className="chat-popup" role="main" aria-label="Chat interface">
      <div className="chat-header" role="banner">
        <div className="header-info">
          <h3>AI Assistant</h3>
          <p>
            <span className="status-indicator" aria-label="Online"></span> RAG Chatbot
          </p>
        </div>
        <button
          className="close-button"
          onClick={closeChat}
          aria-label="Close chat"
        >
          ✕
        </button>
      </div>

      {/* Selected Text Display */}
      {selectedText && (
        <div className="selected-text-preview">
          <p><strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</p>
          <button
            className="use-selection-button"
            onClick={handleSelectedTextClick}
            disabled={isLoading}
          >
            Ask AI about this
          </button>
        </div>
      )}

      <div
        className="chat-messages"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        tabIndex={0}
      >
        {messages.length === 0 ? (
          <div className="welcome-message" role="status" aria-live="polite">
            {backendStatus === 'checking' ? (
              <p>Checking backend connection...</p>
            ) : backendStatus === 'error' ? (
              <div>
                <p>⚠️ Backend service may be unavailable.</p>
                <p>Please check if the backend service is running.</p>
              </div>
            ) : (
              <p>Hello! How can I help you today?</p>
            )}
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.role}-message`}
              role="listitem"
              aria-label={`${message.role} message: ${message.content}`}
            >
              <div className="message-content">
                {message.role === 'bot' ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      code({node, className, children, ...props}) {
                        const match = /language-(\w+)/.exec(className || '');
                        const inline = !match;
                        return !inline && match ? (
                          <pre className={className} role="code">
                            <code {...props}>{children}</code>
                          </pre>
                        ) : (
                          <code className={className} {...props}>{children}</code>
                        );
                      }
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  <span>{message.content}</span>
                )}
              </div>
              <div className="message-timestamp" aria-hidden="true">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message" role="status" aria-live="polite">
            <div className="message-content">
              <span className="typing-indicator" aria-label="Bot is typing">
                <span>Typing</span>
                <span></span>
                <span></span>
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} aria-hidden="true" />
      </div>

      <form
        className="chat-input-form"
        onSubmit={handleSubmit}
        role="form"
        aria-label="Chat input form"
      >
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type a message"
          disabled={isLoading}
          className="chat-input"
          aria-label="Type your message"
          role="textbox"
          aria-multiline="false"
          autoComplete="off"
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
          aria-label="Send message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
          </svg>
        </button>
      </form>

      {error && (
        <div className="error-message" role="alert" aria-live="assertive">
          {error}
        </div>
      )}
    </div>
  );
};

export default ChatWidget;