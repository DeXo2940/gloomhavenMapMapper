import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import EditIcon from '@mui/icons-material/Edit';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import Scenario from '../../types/scenario';
import ScenarioGrid from './ScenarioGrid';
import { scenarioUrl } from '../../config/config';
import GridAdditionalElement from '../../types/gridAdditionalElement';

const ScenarioDetails: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [scenario, setScenario] = useState<Scenario>();
    const navigate = useNavigate();

    useEffect(() => {
        axios.get<Scenario>(scenarioUrl + `/${id}`)
            .then((response) => setScenario(response.data))
            .catch((error) => console.error('Error fetching scenario details:', error));
    }, [id]);

    const handleEditNavigation = async (e: React.FormEvent) => {
        e.preventDefault();
        if (scenario) {
            const edit_navigation = "/edit/" + scenario._id.toString()
            navigate(edit_navigation);
        }
        else {
            // TODO warning - it shouldn't happen
        }

    };

    const spacer_element: GridAdditionalElement = { element: <></>, xs: 7 }
    const edit_button_element = { element: <Button variant="contained" startIcon={<EditIcon />} onClick={handleEditNavigation} fullWidth>Edit</Button>, xs: 1 }
    const element_list = [spacer_element, edit_button_element]

    return (
        <Box>
            <h1>Scenario </h1>
            {scenario ? (
                <ScenarioGrid scenario={scenario} additionalElements={element_list} />
            ) : (
                <p>Loading...</p>
            )
            }
        </Box >
    );
};

export default ScenarioDetails;
