import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import Button from '@mui/material/Button';

import Scenario from '../types/scenario';
import { scenarioUrl } from '../config/config';
import ScenarioGrid from './ScenarioGrid';

const ScenarioForm: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const edit_existing = id != undefined
    const navigate = useNavigate();
    const [scenario, setScenario] = useState<Scenario>({ _id: 1, name: '', coordinates: '' });

    useEffect(() => {
        if (edit_existing) {
            axios.get<Scenario>(scenarioUrl + `/${id}`)
                .then((response) => setScenario(response.data))
                .catch((error) => console.error('Error fetching scenario details:', error));
        }
    }, [id]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        console.log(e.target.name, e.target.value)
        setScenario((prevScenario) => ({
            ...prevScenario,
            [name]: value,
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log(scenario)
        try {
            edit_existing ? await axios.put(scenarioUrl, scenario) : await axios.post(scenarioUrl, scenario)
            // navigate('/'); 
        } catch (error) { console.error('Error submitting the form:', error); }
    };

    const submit_button = <Button variant="contained" startIcon={edit_existing ? <EditIcon /> : <AddIcon />} type="submit" onClick={handleSubmit} fullWidth>
        {edit_existing ? 'Update' : 'Create'}
    </Button>

    return (
        <Box component="form" noValidate autoComplete="off">
            <h1>{edit_existing ? 'Update Scenario' : 'Create Scenario'}</h1>
            <ScenarioGrid
                scenario={scenario}
                editable={true} onChange={handleInputChange}
                additionalElements={[submit_button]}
            />
        </Box >
    );
};

export default ScenarioForm;
