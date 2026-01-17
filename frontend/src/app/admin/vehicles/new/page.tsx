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
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useRouter } from 'next/navigation';

const categories = ['Osobowy', 'SUV', 'Dostawczy', 'Premium'];
const fuels = ['Benzyna', 'Diesel', 'Hybryda', 'Elektryczny'];
const transmissions = ['Manualna', 'Automatyczna'];
const drives = ['FWD', 'RWD', 'AWD', '4x4'];
const promotionOptionsList = ['od ręki', 'promocja', 'Chińczyk', 'Nowość', 'Super Cena'];

const featureGroups = [
    { key: 'audio_multimedia', label: 'Audio i multimedia' },
    { key: 'comfort_extras', label: 'Komfort i dodatki' },
    { key: 'driver_assistance', label: 'Systemy wspomagania kierowcy' },
    { key: 'performance_tuning', label: 'Osiągi i tuning' },
    { key: 'safety', label: 'Bezpieczeństwo' },
];

export default function NewVehicleForm() {
    const router = useRouter();
    const [loading, setLoading] = React.useState(false);
    const [formData, setFormData] = React.useState({
        make: '',
        model: '',
        trim: '',
        year: '',
        registration: '',
        title: '',
        description: '',
        category: '',
        fuel: '',
        transmission: '',
        drive: '',
        color: '',
        price_catalog: '',
        displacement: '',
        power: '',
        seats: '',
        doors: '',
    });

    const [promotions, setPromotions] = React.useState<string[]>([]);

    // Store raw text for features to allow multiline editing
    const [featuresText, setFeaturesText] = React.useState<Record<string, string>>({
        audio_multimedia: '',
        comfort_extras: '',
        driver_assistance: '',
        performance_tuning: '',
        safety: '',
    });

    const [coverImage, setCoverImage] = React.useState<File | null>(null);
    const [galleryImages, setGalleryImages] = React.useState<File[]>([]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleFeatureTextChange = (groupKey: string, value: string) => {
        setFeaturesText(prev => ({ ...prev, [groupKey]: value }));
    };

    const handlePromotionChange = (option: string) => {
        setPromotions(prev => {
            if (prev.includes(option)) {
                return prev.filter(p => p !== option);
            } else {
                return [...prev, option];
            }
        });
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: 'cover' | 'gallery') => {
        if (e.target.files && e.target.files.length > 0) {
            if (type === 'cover') {
                setCoverImage(e.target.files[0]);
            } else {
                setGalleryImages(Array.from(e.target.files));
            }
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // Parse features text into arrays
            const parsedFeatures: Record<string, string[]> = {};
            Object.entries(featuresText).forEach(([key, text]) => {
                parsedFeatures[key] = text.split('\n').map(line => line.trim()).filter(line => line.length > 0);
            });

            // 1. Create Vehicle
            const vehiclePayload = {
                title: formData.title || `${formData.make} ${formData.model} ${formData.trim ? formData.trim + ' ' : ''}${formData.year}`,
                make: formData.make,
                model: formData.model,
                trim: formData.trim,
                year: parseInt(formData.year) || 0,
                description: formData.description,
                color: formData.color,
                price_catalog: parseInt(formData.price_catalog) || 0,
                promotion_options: promotions,
                is_published: true,
                spec_json: {
                    category: formData.category,
                    fuel: formData.fuel,
                    transmission: formData.transmission,
                    drive: formData.drive,
                    displacement: parseInt(formData.displacement) || 0,
                    power: parseInt(formData.power) || 0,
                    seats: parseInt(formData.seats) || 0,
                    doors: parseInt(formData.doors) || 0,
                    features: parsedFeatures,
                }
            };

            const response = await fetch('http://localhost:8000/backoffice/vehicles-catalog', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vehiclePayload),
            });

            if (!response.ok) throw new Error('Failed to create vehicle');
            const vehicle = await response.json();

            // 2. Upload Images
            if (coverImage) {
                const coverData = new FormData();
                coverData.append('file', coverImage);
                coverData.append('is_cover', 'true');
                await fetch(`http://localhost:8000/backoffice/vehicles-catalog/${vehicle.id}/images`, {
                    method: 'POST',
                    body: coverData,
                });
            }

            for (const img of galleryImages) {
                const galleryData = new FormData();
                galleryData.append('file', img);
                galleryData.append('is_cover', 'false');
                await fetch(`http://localhost:8000/backoffice/vehicles-catalog/${vehicle.id}/images`, {
                    method: 'POST',
                    body: galleryData,
                });
            }

            alert('Pojazd dodany pomyślnie!');
            router.push('/admin/vehicles');

        } catch (error) {
            console.error(error);
            alert('Wystąpił błąd podczas dodawania pojazdu.');
        } finally {
            setLoading(false);
        }
    };

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
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="make" label="Marka" fullWidth required onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="model" label="Model" fullWidth required onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="trim" label="Wersja (Trim)" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="year" label="Rok produkcji" type="number" fullWidth required onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="registration" label="Numer Rejestracyjny" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="color" label="Kolor" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 12 }}>
                            <TextField name="description" label="Opis pojazdu" fullWidth multiline rows={3} onChange={handleChange} />
                        </Grid>

                        {/* Opcje Promocji */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="subtitle1" gutterBottom sx={{ mt: 1 }}>Opcje Wyróżnienia</Typography>
                            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                                {promotionOptionsList.map(option => (
                                    <FormControlLabel
                                        key={option}
                                        control={<Checkbox checked={promotions.includes(option)} onChange={() => handlePromotionChange(option)} />}
                                        label={option}
                                    />
                                ))}
                            </Box>
                        </Grid>

                        {/* Specyfikacja */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Specyfikacja</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 3 }}>
                            <TextField select name="category" label="Kategoria" fullWidth defaultValue="" onChange={handleChange}>
                                {categories.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 3 }}>
                            <TextField select name="fuel" label="Paliwo" fullWidth defaultValue="" onChange={handleChange}>
                                {fuels.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 3 }}>
                            <TextField select name="transmission" label="Skrzynia biegów" fullWidth defaultValue="" onChange={handleChange}>
                                {transmissions.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 3 }}>
                            <TextField select name="drive" label="Napęd" fullWidth defaultValue="" onChange={handleChange}>
                                {drives.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        {/* Technical Specs */}
                        <Grid size={{ xs: 6, sm: 3 }}>
                            <TextField name="displacement" label="Pojemność (cm3)" type="number" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 6, sm: 3 }}>
                            <TextField name="power" label="Moc (KM)" type="number" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 6, sm: 3 }}>
                            <TextField name="seats" label="Liczba miejsc" type="number" fullWidth onChange={handleChange} />
                        </Grid>
                        <Grid size={{ xs: 6, sm: 3 }}>
                            <TextField name="doors" label="Liczba drzwi" type="number" fullWidth onChange={handleChange} />
                        </Grid>

                        {/* Wyposażenie */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Wyposażenie</Typography>
                            <Typography variant="caption" color="text.secondary">
                                Wklej listę elementów wyposażenia, każdy w nowej linii.
                            </Typography>
                        </Grid>
                        {featureGroups.map((group) => (
                            <Grid size={{ xs: 12, md: 6 }} key={group.key}>
                                <TextField
                                    label={group.label}
                                    multiline
                                    rows={4}
                                    fullWidth
                                    placeholder={`Opcja 1\nOpcja 2\nOpcja 3`}
                                    value={featuresText[group.key]}
                                    onChange={(e) => handleFeatureTextChange(group.key, e.target.value)}
                                />
                            </Grid>
                        ))}

                        {/* Zdjęcia */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Zdjęcia</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <Button
                                variant="outlined"
                                component="label"
                                startIcon={<CloudUploadIcon />}
                                fullWidth
                            >
                                Wybierz Zdjęcie Główne (Cover)
                                <input type="file" hidden accept="image/*" onChange={(e) => handleFileChange(e, 'cover')} />
                            </Button>
                            {coverImage && <Typography variant="caption" display="block">{coverImage.name}</Typography>}
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <Button
                                variant="outlined"
                                component="label"
                                startIcon={<CloudUploadIcon />}
                                fullWidth
                            >
                                Wybierz Galerię (Wiele)
                                <input type="file" hidden multiple accept="image/*" onChange={(e) => handleFileChange(e, 'gallery')} />
                            </Button>
                            {galleryImages.length > 0 && (
                                <Typography variant="caption" display="block">{galleryImages.length} plików wybranych</Typography>
                            )}
                        </Grid>

                        {/* Ceny */}
                        <Grid size={{ xs: 12 }}>
                            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Finanse</Typography>
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField name="price_catalog" label="Cena katalogowa (PLN)" type="number" fullWidth onChange={handleChange} />
                        </Grid>

                        <Grid size={{ xs: 12 }} sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                            <Button
                                variant="contained"
                                size="large"
                                startIcon={<SaveIcon />}
                                onClick={handleSubmit}
                                disabled={loading}
                            >
                                {loading ? 'Zapisywanie...' : 'Zapisz Pojazd'}
                            </Button>
                        </Grid>
                    </Grid>
                </Box>
            </Paper>
        </Box>
    );
}
