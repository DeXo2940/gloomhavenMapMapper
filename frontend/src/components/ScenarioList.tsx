import React from 'react';
import Box from '@mui/material/Box';

import ScenarioLinkList from './ScenarioLinkList';

const ScenarioList: React.FC = () => {
    return (
        <Box>
            <h1>Scenario List</h1>
            <ScenarioLinkList />
        </Box>
    );
};

export default ScenarioList;
