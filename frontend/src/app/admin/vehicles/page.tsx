'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { DataGrid, GridColDef, GridValueGetter } from '@mui/x-data-grid';
import Link from 'next/link';
import AddIcon from '@mui/icons-material/Add';

const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'brand', headerName: 'Marka', width: 130 },
    { field: 'model', headerName: 'Model', width: 130 },
    { field: 'year', headerName: 'Rok', type: 'number', width: 90 },
    { field: 'registration', headerName: 'Rejestracja', width: 130 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'price', headerName: 'Cena/Doba', type: 'number', width: 120 },
];

const rows = [
    { id: 1, brand: 'Toyota', model: 'Corolla', year: 2023, registration: 'WA 12345', status: 'Dostępny', price: 150 },
    { id: 2, brand: 'Kia', model: 'Sportage', year: 2024, registration: 'KR 54321', status: 'Wynajęty', price: 220 },
    { id: 3, brand: 'BMW', model: '320i', year: 2023, registration: 'PO 99887', status: 'Dostępny', price: 350 },
    { id: 4, brand: 'Skoda', model: 'Octavia', year: 2022, registration: 'DW 11223', status: 'Serwis', price: 180 },
    { id: 5, brand: 'Audi', model: 'A4', year: 2023, registration: 'GD 55667', status: 'Dostępny', price: 300 },
];

export default function VehicleList() {
    return (
        <Box sx={{ height: 600, width: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h4" component="h1">
                    Pojazdy
                </Typography>
                <Button variant="contained" startIcon={<AddIcon />} component={Link} href="/admin/vehicles/new">
                    Dodaj Pojazd
                </Button>
            </Box>
            <DataGrid
                rows={rows}
                columns={columns}
                initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 5 },
                    },
                }}
                pageSizeOptions={[5, 10]}
                checkboxSelection
            />
        </Box>
    );
}
