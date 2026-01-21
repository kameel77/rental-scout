'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import SaveIcon from '@mui/icons-material/Save';

export default function CalculatorConfig() {
    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h4" gutterBottom>
                Konfiguracja Kalkulatora
            </Typography>

            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                    Parametry Najmu (Rent)
                </Typography>
                <Grid container spacing={3}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField label="Bazowa Marża (%)" type="number" fullWidth defaultValue="20" />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField label="Podatek (%)" type="number" fullWidth defaultValue="23" />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField label="Kaucja minimalna (PLN)" type="number" fullWidth defaultValue="1000" />
                    </Grid>
                </Grid>
            </Paper>

            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                    Opcje Dodatkowe
                </Typography>
                <Grid container spacing={3}>
                    <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField label="Ubezpieczenie Pełne (PLN/dzień)" type="number" fullWidth defaultValue="50" />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField label="Dodatkowy Kierowca (PLN/dzień)" type="number" fullWidth defaultValue="20" />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 4 }}>
                        <TextField label="Fotelik Dziecięcy (PLN/dzień)" type="number" fullWidth defaultValue="15" />
                    </Grid>
                </Grid>
            </Paper>

            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                    Parametry Finansowe (Leasing)
                </Typography>
                <Grid container spacing={3}>
                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField label="Oprocentowanie Bazowe (%)" type="number" fullWidth defaultValue="8.5" />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 6 }}>
                        <TextField label="Prowizja Banku (%)" type="number" fullWidth defaultValue="2.0" />
                    </Grid>
                </Grid>
            </Paper>

            <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                <Button variant="contained" size="large" startIcon={<SaveIcon />}>
                    Zapisz Konfigurację
                </Button>
            </Box>
        </Box>
    );
}
