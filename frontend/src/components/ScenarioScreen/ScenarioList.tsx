import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import Scenario from '../../types/scenario';
import { List, ListItemButton, ListItemText } from '@mui/material';
import { scenarioUrl, scenarioUrlSufix, scenarioUrlSufixId } from '../../config/config';

const ScenarioList: React.FC = () => {
    const [scenarios, setScenarios] = useState<Scenario[]>([]);
    const [selectedIndex, setSelectedIndex] = React.useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get<Scenario[]>(scenarioUrl)
            .then((response) => {
                setScenarios(response.data);
            })
            .catch((error) => {
                console.error('Error fetching scenarios:', error);
            });
    }, []);

    const handleListItemClick = (
        event: React.MouseEvent<HTMLDivElement, MouseEvent>, index: number, id: number
    ) => {
        setSelectedIndex(index);
        //TODO navigate is temporary - it will modify the id on the main MasterDetail layout screen
        navigate(scenarioUrlSufixId(id))
    };

    return (
        <List>
            {scenarios.map((scenario, index) => (
                <ListItemButton key={scenario._id} onClick={(event) => handleListItemClick(event, index, scenario._id)} selected={selectedIndex === index}>
                    <ListItemText primary={`#${scenario._id}`} style={{ minWidth: '4ch', maxWidth: '4ch' }} />
                    <ListItemText primary={scenario.name} style={{ textAlign: 'left' }} />
                </ListItemButton>
            ))
            }
        </List >
    );
};

export default ScenarioList;
