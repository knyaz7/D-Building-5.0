import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import "./Gradient.css"
import Home from './Home/Main'
import '@fontsource/jura/300.css'; // Light
import '@fontsource/jura/400.css'; // Regular
import '@fontsource/jura/500.css'; // Medium
import '@fontsource/jura/700.css'; // Bold

function App() {
  return (
    <Router> 
      <div className="App">   
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
        <div class="gradient"></div>
      </div>
    </Router>
  );
}
    
export default App;