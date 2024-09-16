import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function Chatbot() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const sendMessage = async () => {
    const newMessages = [...messages, { text: message, type: 'sent' }];
    setMessages(newMessages);
    setMessage('');
    try {
      const res = await axios.post('http://localhost:5000/chat', { message });
      setMessages([...newMessages, { text: res.data.data, type: 'received' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...newMessages, { text: 'Sorry, something went wrong.', type: 'received' }]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="container mt-5">
      <div id="chat" style={{ backgroundColor: 'grey', padding: '10px', height: '300px', overflowY: 'scroll' }}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              backgroundColor: msg.type === 'sent' ? 'lightblue' : 'white',
              padding: '5px',
              marginBottom: '5px',
              borderRadius: '5px',
              maxWidth: '100%',
              alignSelf: msg.type === 'sent' ? 'flex-end' : 'flex-start',
            }}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} /> {/* Empty div for scrolling */}
      </div>
      <form onSubmit={handleSubmit} className="mt-3">
        <div className="form-group">
          <label htmlFor="message">Message:</label>
          <input
            type="text"
            className="form-control"
            id="message"
            value={message}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit" className="btn btn-primary mt-3">Send</button>
      </form>
    </div>
  );
}

export default Chatbot;
