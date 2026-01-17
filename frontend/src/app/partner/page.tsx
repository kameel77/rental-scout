'use client';
import * as React from 'react';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function StatCard({ title, value }: { title: string, value: string | number }) {
    return (
        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
                {title}
            </Typography>
            <Typography component="p" variant="h4">
                {value}
            </Typography>
        </Paper>
    );
}

export default function PartnerDashboard() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" gutterBottom component="div">
                Partner Dashboard
            </Typography>
            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6 }}>
                    <StatCard title="Moje Kalkulacje" value={14} />
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                    <StatCard title="Moje Leady" value={3} />
                </Grid>
            </Grid>
        </Box>
    );
}
