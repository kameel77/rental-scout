'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import MenuItem from '@mui/material/MenuItem';
import SaveIcon from '@mui/icons-material/Save';

const categories = ['Osobowy', 'SUV', 'Dostawczy', 'Premium'];
const fuels = ['Benzyna', 'Diesel', 'Hybryda', 'Elektryczny'];
const transmissions = ['Manualna', 'Automatyczna'];

export default function NewVehicleForm() {
    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h4" gutterBottom>
                Dodaj Nowy Pojazd
            </Typography>
            <Paper sx={{ p: 3 }}>
                <Box component="form" noValidate autoComplete="off">
                    <Grid container spacing={3}>
                        {/* Dane podstawowe */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom>Dane Podstawowe</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField required label="Marka" fullWidth />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField required label="Model" fullWidth />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField required label="Rok produkcji" type="number" fullWidth />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField required label="Numer Rejestracyjny" fullWidth />
                        </Grid>

                        {/* Specyfikacja */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Specyfikacja</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField select label="Kategoria" fullWidth defaultValue="">
                                {categories.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField select label="Paliwo" fullWidth defaultValue="">
                                {fuels.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField select label="Skrzynia biegów" fullWidth defaultValue="">
                                {transmissions.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        {/* Wyposażenie */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Wyposażenie</Typography>
                        </Grid>
                        <Grid size={{ xs: 12 }}>
                            <FormControlLabel control={<Checkbox />} label="Klimatyzacja" />
                            <FormControlLabel control={<Checkbox />} label="Nawigacja" />
                            <FormControlLabel control={<Checkbox />} label="Tempomat" />
                            <FormControlLabel control={<Checkbox />} label="Czujniki parkowania" />
                            <FormControlLabel control={<Checkbox />} label="Kamera cofania" />
                        </Grid>

                        {/* Ceny */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Cennik (PLN)</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField label="Stawka dobowa" type="number" fullWidth />
                        </Grid>

                        <Grid size={{ xs: 12 }} sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                            <Button variant="contained" size="large" startIcon={<SaveIcon />}>
                                Zapisz Pojazd
                            </Button>
                        </Grid>
                    </Grid>
                </Box>
            </Paper>
        </Box>
    );
}
