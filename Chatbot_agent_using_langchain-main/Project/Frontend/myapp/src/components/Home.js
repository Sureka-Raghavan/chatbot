import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import Chatbot from './Chatbot'; // Adjust the import based on your file structure

function Home() {
  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
        <div className="bg-light p-4" style={{ backgroundColor: 'ash', width: '80%', height: '80vh' }}>
            <div>
                <Chatbot/>
            </div>
        </div>
    </div>
  );
}

export default Home;
