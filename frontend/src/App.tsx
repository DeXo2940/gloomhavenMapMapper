import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Assuming you are using BrowserRouter

import ScenarioList from './components/ScenarioList';
import ScenarioDetails from './components/ScenarioDetails';
import ScenarioForm from './components/ScenarioForm';
import ScenarioLayout from './components/ScenarioLayout';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScenarioList />} />
        <Route path="/scenarios" element={<ScenarioList />} />
        <Route path="/scenarios/:id" element={<ScenarioDetails />} />
        <Route path="/create" element={<ScenarioForm />} />
        <Route path="/edit/:id" element={<ScenarioForm />} />
        <Route path="/layout" element={<ScenarioLayout />} />
      </Routes>
    </Router>
  );
};

export default App;
