'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'client', headerName: 'Klient', width: 200 },
    { field: 'vehicle', headerName: 'Pojazd', width: 180 },
    { field: 'status', headerName: 'Status', width: 130 },
];

const rows = [
    { id: 1, client: 'Firma X', vehicle: 'BMW 320i', status: 'Ofertowanie' },
    { id: 2, client: 'Janusz nosacz', vehicle: 'Toyota Corolla', status: 'Zakończony' },
];

export default function PartnerLeads() {
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography variant="h4" gutterBottom>Moje Leady</Typography>
            <DataGrid rows={rows} columns={columns} />
        </Box>
    );
}
