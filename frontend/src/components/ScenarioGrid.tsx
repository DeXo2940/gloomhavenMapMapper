import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import IdTextField from './FormTextField/IdTextField';
import CoordinatesTextField from './FormTextField/CoordinatesTextField';
import ScenarioNameTextField from './FormTextField/ScenarioNameTextField';

import Scenario from '../types/scenario';
import { scenarioUrl } from '../config/config';

interface ScenarioGridProps {
    scenario: Scenario;
    editable?: boolean;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
    additionalElements?: [React.ReactNode];
    xs_size?: number;
}

const ScenarioGrid: React.FC<ScenarioGridProps> = ({ scenario, editable = false, onChange, additionalElements = [], xs_size = 8 }) => {
    const { id } = useParams<{ id: string }>();
    const is_edit = id != undefined
    const [template_scenario, setTemplateScenario] = useState<Scenario>({ _id: 1, name: 'Name', coordinates: 'A-1' });

    useEffect(() => {
        const templateScenarioUrl = is_edit ? scenarioUrl + `/${id}` : scenarioUrl + `/1`;
        axios.get<Scenario>(templateScenarioUrl)
            .then((response) => setTemplateScenario(response.data))
    }, [id]);

    return (
        <Grid container spacing={2} xs={xs_size} >
            <Grid xs={xs_size / 2} >
                <IdTextField value={scenario._id} onChange={onChange} placeholder={template_scenario._id} editable={!is_edit && editable} />
            </Grid>
            <Grid xs={xs_size / 2} >
                <CoordinatesTextField value={scenario.coordinates} onChange={onChange} placeholder={template_scenario.coordinates} editable={editable} />
            </Grid>
            <br />
            <Grid xs={xs_size} >
                <ScenarioNameTextField value={scenario.name} onChange={onChange} placeholder={template_scenario.name} editable={editable} />
            </Grid>
            {additionalElements.map((element, index) => (
                <Grid xs={xs_size}>
                    {element}
                </Grid>
            ))}
        </Grid>
    )
};

export default ScenarioGrid;