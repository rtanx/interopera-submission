'use client'

import { useState, useRef, useEffect } from 'react';

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

        // Add user message
        const userMessage = {
            id: Date.now(),
            sender: 'user',
            text: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        // Simulate AI response (TODO: replace with actual API call)
        setTimeout(() => {
            // Example response based on user input
            let responseText = "I'm processing your query about sales data. In a real implementation, this would connect to your backend AI service.";

            if (inputValue.toLowerCase().includes('performance')) {
                responseText = "Performance analysis would show metrics like close rates, average deal size, and revenue trends. In the full implementation, I'd provide specific insights based on the data.";
            } else if (inputValue.toLowerCase().includes('deal') || inputValue.toLowerCase().includes('sales')) {
                responseText = "I can help analyze deal pipelines, conversion rates, and forecast future sales based on historical data. The complete implementation would connect to your sales database.";
            }

            const aiMessage = {
                id: Date.now(),
                sender: 'ai',
                text: responseText,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, aiMessage]);
            setIsLoading(false);
        }, 1000);
    };

    return (
        <div className="flex flex-col h-full max-h-[600px]">
            <div className="bg-blue-600 text-white p-3 rounded-t-lg">
                <h2 className="font-semibold">Sales Assistant</h2>
            </div>

            {/* Chat messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-lg ${message.sender === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-white border border-gray-200'
                                }`}
                        >
                            <p>{message.text}</p>
                            <p className={`text-xs mt-1 ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                                }`}>
                                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
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