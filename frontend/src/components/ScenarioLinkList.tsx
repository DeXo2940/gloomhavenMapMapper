import React, { useEffect, useState } from 'react';
import axios from 'axios';

import Scenario from '../types/scenario';
import { Box, List, ListItem, ListItemButton, ListItemText } from '@mui/material';

const ScenarioLinkList: React.FC = () => {
    const [scenarios, setScenarios] = useState<Scenario[]>([]);

    useEffect(() => {
        axios.get<Scenario[]>('http://localhost:5000/scenarios')
            .then((response) => {
                setScenarios(response.data);
            })
            .catch((error) => {
                console.error('Error fetching scenarios:', error);
            });
    }, []);

    return (
        <List>
            {scenarios.map((scenario) => (
                <ListItemButton key={scenario._id} component="a" href={`/scenarios/${scenario._id}`}>
                    <ListItemText primary={`#${scenario._id}`} style={{ minWidth: '4ch', maxWidth: '4ch' }} />
                    <ListItemText primary={scenario.name} style={{ textAlign: 'left' }} />
                </ListItemButton>
            ))}
        </List>
    );
};

export default ScenarioLinkList;
