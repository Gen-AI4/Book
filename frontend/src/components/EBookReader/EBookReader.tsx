import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { sendChatMessage, ChatRequest, ChatResponse } from '../../services/chat-api';
import './EBookReader.css';

// Define TypeScript interfaces
interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'bot';
  timestamp: Date;
}

interface DocumentContent {
  id: string;
  title: string;
  content: string;
  sidebar_position: number;
}

interface Chapter {
  id: string;
  title: string;
  items?: Chapter[];
}

const EBookReader: React.FC = () => {
  // State management
  const [selectedText, setSelectedText] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [currentDocument, setCurrentDocument] = useState<DocumentContent | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<string>('foundations');

  // Refs
  const contentRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Sample document content - in a real app this would come from the docs
  const documentContent: DocumentContent[] = [
    {
      id: 'foundations',
      title: 'Foundations',
      sidebar_position: 1,
      content: `# Foundations

Welcome to the Physical AI & Humanoid Robotics textbook. This module provides the foundational knowledge required to understand the intersection of artificial intelligence and physical systems.

## Learning Objectives

By the end of this module, you will understand:
- The fundamental concepts of Physical AI
- How AI systems interact with physical reality
- The core principles of humanoid robotics
- The relationship between simulation and real-world deployment

## What is Physical AI?

Physical AI represents the convergence of artificial intelligence with physical systems. Unlike traditional AI that operates in digital spaces, Physical AI must navigate, interact with, and adapt to the complexities of the physical world.

### Key Characteristics

- **Embodied Intelligence**: AI systems that exist and operate within physical bodies
- **Real-time Processing**: Systems that must respond to physical stimuli in real-time
- **Uncertainty Management**: Handling sensor noise, actuator limitations, and environmental unpredictability
- **Safety-Critical Operations**: Systems where failure can have physical consequences

## Hardware Considerations

Throughout this curriculum, we'll reference specific hardware platforms that exemplify Physical AI concepts:

- **Unitree Humanoid Platforms**: Advanced humanoid robots for research and development
- **NVIDIA Jetson Orin**: AI computing platform for robotics applications
- **RTX 40-series GPUs**: For simulation and real-time inference
- **ROS 2 Compatible Sensors**: LiDAR, cameras, IMUs, and other perception hardware

> [!hardware]
> **Hardware Note**: The concepts in this textbook are applicable to various robotic platforms, but examples will reference the Unitree humanoid platform and NVIDIA Jetson Orin for specific implementation details.

## Next Steps

In the following chapters, we'll explore embodied intelligence, hardware lab setup, and the course roadmap that connects these foundational concepts to practical implementations.`
    },
    {
      id: 'embodied-intelligence',
      title: 'Embodied Intelligence',
      sidebar_position: 2,
      content: `# Embodied Intelligence

Embodied intelligence is a fundamental concept in robotics and AI that emphasizes the role of a physical body in the development of intelligent behavior.

## Core Principles

Embodied intelligence is based on three core principles:

1. **Morphological Computation**: The body's physical properties contribute to intelligent behavior
2. **Environment Interaction**: Intelligence emerges through interaction with the environment
3. **Sensorimotor Coupling**: Perception and action are tightly coupled in intelligent systems

## Examples in Nature

- Animals use their body structure to simplify complex tasks
- Octopi use their flexible arms for dexterous manipulation
- Birds use their wing structure for efficient flight dynamics

## Applications in Robotics

In humanoid robotics, embodied intelligence principles are applied through:

- Compliant actuators that adapt to environmental constraints
- Sensor-rich body structures for rich environmental feedback
- Morphological features that simplify control problems`
    }
  ];

  // Sample sidebar structure
  const sidebarStructure: Chapter[] = [
    {
      id: 'intro',
      title: 'Introduction',
      items: [
        { id: 'foundations', title: 'Foundations' },
        { id: 'embodied-intelligence', title: 'Embodied Intelligence' },
        { id: 'hardware-lab', title: 'Hardware Lab Setup' },
        { id: 'course-roadmap', title: 'Course Roadmap' }
      ]
    },
    {
      id: 'module1',
      title: 'Module 1: ROS 2 Foundations',
      items: [
        { id: 'ros2-intro', title: 'Introduction to ROS 2' },
        { id: 'nodes-topics', title: 'Nodes and Topics' },
        { id: 'services-actions', title: 'Services and Actions' }
      ]
    }
  ];

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

  // Load document when selected chapter changes
  useEffect(() => {
    const doc = documentContent.find(d => d.id === selectedChapter);
    if (doc) {
      setCurrentDocument(doc);
    }
  }, [selectedChapter]);

  // Function to send message to backend
  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue;
    if (!textToSend.trim() || isLoading) return;

    try {
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

      // Set loading state
      setIsLoading(true);

      // Prepare the API request
      const requestBody: ChatRequest = {
        message: textToSend,
        session_id: sessionId || undefined,
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

  // Handle text selection click (send selected text to chat)
  const handleSelectedTextClick = () => {
    if (selectedText) {
      sendMessage(selectedText);
      setSelectedText(''); // Clear selection after sending
    }
  };

  // Toggle sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="ebook-reader">
      {/* Sidebar */}
      <div className={`ebook-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h3>Table of Contents</h3>
          <button className="sidebar-toggle" onClick={toggleSidebar}>
            {sidebarOpen ? '«' : '»'}
          </button>
        </div>

        <div className="sidebar-content">
          {sidebarStructure.map((section) => (
            <div key={section.id} className="sidebar-section">
              <h4>{section.title}</h4>
              {section.items && (
                <ul>
                  {section.items.map((item) => (
                    <li
                      key={item.id}
                      className={`sidebar-item ${selectedChapter === item.id ? 'active' : ''}`}
                      onClick={() => setSelectedChapter(item.id)}
                    >
                      {item.title}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="ebook-main">
        <div className="ebook-content" ref={contentRef}>
          {currentDocument ? (
            <div className="document-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({node, inline, className, children, ...props}) {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <pre className={className}>
                        <code {...props}>{children}</code>
                      </pre>
                    ) : (
                      <code className={className} {...props}>{children}</code>
                    );
                  },
                  blockquote({node, ...props}) {
                    return (
                      <blockquote {...props} className="admonition-hardware">
                        {props.children}
                      </blockquote>
                    );
                  }
                }}
              >
                {currentDocument.content}
              </ReactMarkdown>
            </div>
          ) : (
            <div className="no-document">Select a chapter from the sidebar</div>
          )}
        </div>

        {/* Chat Panel */}
        <div className="ebook-chat-panel">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <div className="header-actions">
              <span className="status-indicator" aria-label="Online"></span>
              <span>RAG Chatbot</span>
            </div>
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

          {/* Chat Messages */}
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Select text in the document and click "Ask AI about this" to get explanations, summaries, or clarifications.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role}-message`}
                >
                  <div className="message-content">
                    {message.role === 'bot' ? (
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          code({node, inline, className, children, ...props}) {
                            const match = /language-(\w+)/.exec(className || '');
                            return !inline && match ? (
                              <pre className={className}>
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
                  <div className="message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <span className="typing-indicator">
                    <span>Typing</span>
                    <span></span>
                    <span></span>
                  </span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <form className="chat-input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the content..."
              disabled={isLoading}
              className="chat-input"
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EBookReader;