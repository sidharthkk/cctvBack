
import React from 'react';
import './Welcome.css'; 
import { useNavigate } from 'react-router-dom';

function Welcome() {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/new-page');
    };

    return (
        <body>
        <div className="welcome-container">
            <h1 className="welcome-heading">REAL TIME CRIME DETECTION</h1>
            <button class="setup" onClick={handleClick}>SETUP ENV </button>
          
        </div>
        </body>
    );
}

export default Welcome;
