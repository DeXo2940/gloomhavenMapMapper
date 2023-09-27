import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Assuming you are using BrowserRouter

import ScenarioList from './components/ScenarioList';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScenarioList />} />
      </Routes>
    </Router>
  );
};

export default App;
