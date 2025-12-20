import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Welcome to the Physical AI & Humanoid Robotics textbook assistant. How can I help you today?',
      sender: 'ai',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = () => {
    if (inputValue.trim() === '') return;

    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputValue('');

    // Simulate AI response after a delay
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: `I received your message: "${inputValue}". This is a simulated response from the AI assistant.`,
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        // Expanded Chat Widget
        <div className="bg-cyber-black border-2 border-cyber-neon-green glow-neon w-80 h-96 flex flex-col backdrop-filter backdrop-blur-sm" style={{
          clipPath: 'polygon(0 10px, 10px 0, calc(100% - 10px) 0, 100% 10px, 100% calc(100% - 10px), calc(100% - 10px) 100%, 10px 100%, 0 calc(100% - 10px))'
        }}>
          {/* Chat Header */}
          <div className="bg-cyber-black border-b border-cyber-neon-green p-3 flex justify-between items-center">
            <span className="text-cyber-neon-green font-jetbrains-mono text-sm uppercase tracking-wider">
              AI ASSISTANT
            </span>
            <button
              onClick={toggleChat}
              className="text-cyber-neon-green hover:text-cyber-red transition-colors"
            >
              ✕
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-3 font-jetbrains-mono">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-3 ${message.sender === 'user' ? 'text-right' : 'text-left'}`}
              >
                <div
                  className={`inline-block p-2 rounded ${
                    message.sender === 'user'
                      ? 'bg-cyber-neon-green text-cyber-black'
                      : 'bg-gray-900 border border-cyber-neon-blue text-cyber-neon-blue'
                  }`}
                >
                  {message.text}
                </div>
                <div className="text-xs text-cyber-neon-purple mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 border-t border-cyber-neon-green">
            <div className="flex">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 bg-cyber-black border-2 border-cyber-neon-green text-cyber-neon-green font-jetbrains-mono p-2 focus:outline-none focus:ring-2 focus:ring-cyber-neon-green glow"
              />
              <button
                onClick={handleSend}
                className="ml-2 bg-cyber-neon-green text-cyber-black font-jetbrains-mono font-bold px-4 py-2 hover:bg-transparent hover:text-cyber-neon-green border-2 border-cyber-neon-green transition-colors"
              >
                SEND
              </button>
            </div>
          </div>
        </div>
      ) : (
        // Minimized FAB
        <button
          onClick={toggleChat}
          className="bg-cyber-neon-green text-cyber-black font-jetbrains-mono font-bold w-16 h-16 rounded-full flex items-center justify-center shadow-lg glow-neon animate-pulse"
          aria-label="Open chat"
        >
          AI
        </button>
      )}
    </div>
  );
};

export default ChatWidget;