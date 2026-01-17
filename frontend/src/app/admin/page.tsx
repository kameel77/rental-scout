'use client';
import * as React from 'react';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { BarChart } from '@mui/x-charts/BarChart';
import { PieChart } from '@mui/x-charts/PieChart';

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

export default function AdminDashboard() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" gutterBottom component="div">
                Dashboard
            </Typography>
            <Grid container spacing={3}>
                {/* Stats */}
                <Grid size={{ xs: 12, md: 3 }}>
                    <StatCard title="Pojazdy" value={24} />
                </Grid>
                <Grid size={{ xs: 12, md: 3 }}>
                    <StatCard title="Aktywne Oferty" value={12} />
                </Grid>
                <Grid size={{ xs: 12, md: 3 }}>
                    <StatCard title="Leady" value={8} />
                </Grid>
                <Grid size={{ xs: 12, md: 3 }}>
                    <StatCard title="Partnerzy" value={5} />
                </Grid>

                {/* Charts */}
                <Grid size={{ xs: 12, md: 8 }}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
                        <Typography component="h2" variant="h6" color="primary" gutterBottom>
                            Przychody Miesięczne (PLN)
                        </Typography>
                        <BarChart
                            series={[{ data: [35000, 44000, 24000, 50000, 60000, 55000] }]}
                            xAxis={[{ scaleType: 'band', data: ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze'] }]}
                            margin={{ top: 10, bottom: 30, left: 40, right: 10 }}
                        />
                    </Paper>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
                        <Typography component="h2" variant="h6" color="primary" gutterBottom>
                            Popularność Kategorii
                        </Typography>
                        <PieChart
                            series={[
                                {
                                    data: [
                                        { id: 0, value: 10, label: 'SUV' },
                                        { id: 1, value: 15, label: 'Sedan' },
                                        { id: 2, value: 5, label: 'Kombi' },
                                    ],
                                },
                            ]}
                            margin={{ right: 5 }}
                        />
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
}
