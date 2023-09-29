import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import IdTextField from '../FormTextField/IdTextField';
import CoordinatesTextField from '../FormTextField/CoordinatesTextField';
import ScenarioNameTextField from '../FormTextField/ScenarioNameTextField';

import Scenario from '../../types/scenario';
import GridAdditionalElement from '../../types/gridAdditionalElement';
import { scenarioUrl } from '../../config/config';


interface ScenarioGridProps {
    scenario: Scenario;
    editable?: boolean;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
    additionalElements?: GridAdditionalElement[];
    xs_size?: number;
}

const ScenarioGrid: React.FC<ScenarioGridProps> = ({ scenario, editable = false, onChange, additionalElements = [], xs_size = 8 }) => {
    const { id } = useParams<{ id: string }>();
    const is_edit = id != undefined
    const [template_scenario, setTemplateScenario] = useState<Scenario>({ _id: 1, name: 'Name', coordinates: 'A-1' });
    let sth = true;

    useEffect(() => {
        const templateScenarioUrl = is_edit ? scenarioUrl + `/${id}` : scenarioUrl + `/1`;
        axios.get<Scenario>(templateScenarioUrl)
            .then((response) => setTemplateScenario(response.data))
            .catch((error) => console.error('Error fetching placeholder scenario details:', error));
    }, [id]);

    return (
        < Grid container spacing={2} xs={xs_size} >
            <Grid key='id' xs={xs_size / 2} >
                <IdTextField value={scenario._id} onChange={onChange} placeholder={template_scenario._id} editable={!is_edit && editable} />
            </Grid>
            <Grid key='coordinates' xs={xs_size / 2} >
                <CoordinatesTextField value={scenario.coordinates} onChange={onChange} placeholder={template_scenario.coordinates} editable={editable} />
            </Grid>
            <Grid key='name' xs={xs_size} >
                <ScenarioNameTextField value={scenario.name} onChange={onChange} placeholder={template_scenario.name} editable={editable} />
            </Grid>
            {
                additionalElements.map((grid_element, index) => (
                    <Grid key={`additonal_${index}`} xs={grid_element.xs !== undefined ? grid_element.xs : xs_size}>{grid_element.element}</Grid>
                ))
            }
        </Grid >
    )
};

export default ScenarioGrid;