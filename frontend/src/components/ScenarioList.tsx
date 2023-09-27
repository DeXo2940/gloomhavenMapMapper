import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ScenarioList: React.FC = () => {
    const [scenarios, setScenarios] = useState([]);

    useEffect(() => {
        // Fetch scenarios from the backend
        axios.get('http://localhost:5000/scenarios')
            .then((response) => {
                setScenarios(response.data);
            })
            .catch((error) => {
                console.error('Error fetching scenarios:', error);
            });
    }, []);

    return (
        <div>
            <h1>Scenario List</h1>
            {/* Render the list of scenarios */}
        </div>
    );
};

export default ScenarioList;
