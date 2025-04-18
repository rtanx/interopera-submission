'use client'

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';

export default function AIChatRoom({ selectedRep }) {
    const [messages, setMessages] = useState([
        {
            id: 1,
            sender: 'ai',
            text: 'Hello! I can help you analyze sales data. Select a rep or ask me a question about sales performance.',
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Scroll to bottom when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Add AI message when a rep is selected
    useEffect(() => {
        if (selectedRep) {
            const aiMessage = {
                id: Date.now(),
                sender: 'ai',
                text: `You've selected ${selectedRep.name}. They're a ${selectedRep.role} in the ${selectedRep.region} region with ${selectedRep.deals.length} deals. How can I help you analyze their performance?`,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, aiMessage]);
        }
    }, [selectedRep]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        const userMessage = {
            id: Date.now(),
            sender: 'user',
            text: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const resp = await fetch('/api/ai', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: inputValue,
                    rep_context_id: selectedRep?.id || null
                })
            });

            if (!resp.ok) throw new Error(`Failed to fetch AI response ${resp.status}`);

            const { answer } = await resp.json();

            const aiMessage = {
                id: Date.now() + 1,
                sender: 'ai',
                text: answer,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, aiMessage]);

        } catch (err) {
            console.log('Error fetching AI response:', err);
            setMessages(prev => [
                ...prev,
                {
                    id: Date.now() + 1,
                    sender: 'ai',
                    text: 'Sorry, There was an error processing your request. Please try again.',
                    timestamp: new Date()
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full max-h-[700px]">
            <div className="bg-blue-600 text-white p-3 rounded-t-lg">
                <h2 className="font-semibold">Sales Assistant</h2>
            </div>

            {/* Chat messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map(msg => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-lg ${msg.sender === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-white border border-gray-200'
                                }`}
                        >
                            {msg.sender === 'ai' ? (
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        code({ node, inline, className, children, ...props }) {
                                            const match = /language-(\w+)/.exec(className || '');
                                            return !inline && match ? (
                                                <SyntaxHighlighter
                                                    style={oneDark}
                                                    language={match[1]}
                                                    PreTag="div"
                                                    {...props}
                                                >
                                                    {String(children).replace(/\n$/, '')}
                                                </SyntaxHighlighter>
                                            ) : (
                                                <code className={className} {...props}>
                                                    {children}
                                                </code>
                                            );
                                        }
                                    }}
                                >
                                    {msg.text}
                                </ReactMarkdown>
                            ) : (
                                <p>{msg.text}</p>
                            )}
                            <p className={`text-xs mt-1 ${msg.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                                }`}>
                                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-gray-200 p-3 rounded-lg">
                            <div className="flex space-x-1">
                                <div className="bg-gray-400 rounded-full h-2 w-2 animate-bounce"></div>
                                <div className="bg-gray-400 rounded-full h-2 w-2 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                <div className="bg-gray-400 rounded-full h-2 w-2 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Chat input */}
            <div className="p-3 border-t">
                <form onSubmit={handleSubmit} className="flex space-x-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Ask about sales data..."
                        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className={`bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                        disabled={isLoading}
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}