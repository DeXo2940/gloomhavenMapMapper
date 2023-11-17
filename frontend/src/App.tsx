import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Assuming you are using BrowserRouter

import ScenarioList from './components/ScenarioScreen/ScenarioList';
import ScenarioDetails from './components/ScenarioScreen/ScenarioDetails';
import ScenarioForm from './components/ScenarioScreen/ScenarioForm';
import ScenarioLayout from './components/ScenarioMasterDetailLayout';

import { scenarioUrlSufix, scenarioUrlSufixId, scenarioUrlSufixIdTemplate } from './config/config'

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScenarioList />} />
        <Route path={scenarioUrlSufix} element={<ScenarioList />} />
        <Route path={scenarioUrlSufixIdTemplate} element={<ScenarioDetails />} />
        <Route path="/create" element={<ScenarioForm />} />
        <Route path="/edit/:id" element={<ScenarioForm />} />
        <Route path="/layout" element={<ScenarioLayout />} />
      </Routes>
    </Router>
  );
};

export default App;
