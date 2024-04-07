// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Welcome from './Welcome'; 
import NewPage from './NewPage'; 

function App() {
    return (
        <Router> {/* Wrap your components with the Router component */}
            <Routes>
                <Route path="/" element={<Welcome />} /> {/* Render the Welcome component at the root path */}
                <Route path="/new-page" element={<NewPage />} /> {/* Render the NewPage component at the /new-page path */}
            </Routes>
        </Router>
    );
}

export default App;
