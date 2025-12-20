import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { sendChatMessage, ChatRequest, ChatResponse, ChatError } from '../../services/chat-api';
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
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string>('');

  // Ref for auto-scrolling to bottom
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to send message to backend
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    try {
      // Clear any previous errors
      setError(null);

      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        content: inputValue,
        role: 'user',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage]);

      // Clear input field immediately after sending
      setInputValue('');

      // Set loading state
      setIsLoading(true);

      // Prepare the API request
      const requestBody: ChatRequest = {
        message: inputValue,
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

  return (
    <div className="chat-widget" role="main" aria-label="Chat interface">
      <div className="chat-header" role="banner">
        <h3>Cyber Chat</h3>
      </div>

      <div
        className="chat-messages"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        tabIndex={0}
      >
        {messages.length === 0 ? (
          <div className="welcome-message" role="status" aria-live="polite">
            <p>Hello! How can I help you today?</p>
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
                      code({node, inline, className, children, ...props}) {
                        const match = /language-(\w+)/.exec(className || '');
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
              <span className="typing-indicator" aria-label="Bot is typing">Typing...</span>
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
          placeholder="Type your message..."
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
          Send
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