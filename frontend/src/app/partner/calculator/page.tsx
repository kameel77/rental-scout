'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import CalculateIcon from '@mui/icons-material/Calculate';
import Alert from '@mui/material/Alert';

const vehicles = [
    { id: 1, label: 'Toyota Corolla 2023' },
    { id: 2, label: 'Kia Sportage 2024' },
    { id: 3, label: 'BMW 320i 2023' },
];

export default function PartnerCalculator() {
    const [result, setResult] = React.useState<number | null>(null);

    const handleCalculate = () => {
        setResult(3500); // Mock result
    };

    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h4" gutterBottom>
                Kalkulator Ofert
            </Typography>

            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6 }}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>Danne Oferty</Typography>
                        <Box component="form" noValidate autoComplete="off">
                            <Grid container spacing={2}>
                                <Grid size={{ xs: 12 }}>
                                    <TextField select label="Wybierz Pojazd" fullWidth defaultValue="">
                                        {vehicles.map((v) => (
                                            <MenuItem key={v.id} value={v.id}>{v.label}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6 }}>
                                    <TextField label="Data Od" type="date" fullWidth InputLabelProps={{ shrink: true }} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6 }}>
                                    <TextField label="Data Do" type="date" fullWidth InputLabelProps={{ shrink: true }} />
                                </Grid>
                                <Grid size={{ xs: 12 }}>
                                    <TextField label="Rabat (%)" type="number" fullWidth defaultValue="0" />
                                </Grid>
                                <Grid size={{ xs: 12 }}>
                                    <Button variant="contained" size="large" fullWidth startIcon={<CalculateIcon />} onClick={handleCalculate}>
                                        Oblicz Ofertę
                                    </Button>
                                </Grid>
                            </Grid>
                        </Box>
                    </Paper>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <Paper sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                        {result ? (
                            <>
                                <Typography variant="h5" color="text.secondary">Szacowana kwota:</Typography>
                                <Typography variant="h2" color="primary" sx={{ my: 2 }}>
                                    {result} PLN
                                </Typography>
                                <Button variant="outlined" color="secondary">Generuj PDF</Button>
                            </>
                        ) : (
                            <Typography color="text.secondary">Wprowadź dane aby zobaczyć wynik</Typography>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
}
