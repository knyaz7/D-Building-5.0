import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Home from './Home/Main'
import Add from './AdminAdd'
import ProjectManage from './ProjectManage';
import Welcome from "./Welcome"
import "./Gradient.css"
import '@fontsource/jura/300.css'; // Light
import '@fontsource/jura/400.css'; // Regular
import '@fontsource/jura/500.css'; // Medium
import '@fontsource/jura/700.css'; // Bold
<<<<<<< Updated upstream
=======
import Task from './frontILIA/my-app/src/Tasks'

>>>>>>> Stashed changes

function App() {
  return (
    <Router> 
      <div className="App">   
        <Routes>
          <Route path="/adm-pan/add" element={<Add />} />
          <Route path="/adm-pan" element={<ProjectManage />} />
          <Route path="/" element={<Home />} />
          <Route path="/welcome" element={<Welcome />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
        <div class="gradient"></div>
      </div>
    </Router>
  );
}
    
export default App;