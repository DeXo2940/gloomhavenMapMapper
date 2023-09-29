import React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import { Paper, Typography } from '@mui/material';
import ScenarioList from './ScenarioScreen/ScenarioList';
import ScenarioDetails from './ScenarioScreen/ScenarioDetails';

const ScenarioLayout: React.FC = () => {
    return (
        <Box>
            <h1>Hello it's layout</h1>
            <Grid container spacing={2}>
                <Grid xs={2}>
                    <Paper elevation={3}>
                        <Typography variant="h6">Scenarios</Typography>
                        <ScenarioList />
                    </Paper>
                </Grid>
                <Grid xs={10}>
                    <Paper elevation={3}>
                        <Typography variant="h6">Details</Typography>
                        <ScenarioDetails />
                    </Paper>
                </Grid>
            </Grid>

        </Box>
    )
};

export default ScenarioLayout;