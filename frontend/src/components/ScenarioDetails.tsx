import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import IdTextField from './FormTextField/IdTextField';
import CoordinatesTextField from './FormTextField/CoordinatesTextField';
import ScenarioNameTextField from './FormTextField/ScenarioNameTextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import Scenario from '../types/scenario';
import ScenarioGrid from './ScenarioGrid';

const ScenarioDetails: React.FC = () => {
    const scenarioUrl = 'http://localhost:5000/scenarios'

    const { id } = useParams<{ id: string }>();
    const [scenario, setScenario] = useState<Scenario | null>(null);

    useEffect(() => {
        axios.get<Scenario>(scenarioUrl + `/${id}`)
            .then((response) => setScenario(response.data))
            .catch((error) => console.error('Error fetching scenario details:', error));
    }, [id]);

    return (
        <Box>
            <h1>Scenario </h1>
            {scenario ? (
                <ScenarioGrid scenario={scenario} />
            ) : (
                <p>Loading...</p>
            )}
        </Box>
    );
};

export default ScenarioDetails;
