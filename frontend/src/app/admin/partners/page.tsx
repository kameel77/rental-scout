'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Nazwa Partnera', width: 200 },
    { field: 'contact', headerName: 'Osoba Kontaktowa', width: 200 },
    { field: 'status', headerName: 'Status', width: 130 },
];

const rows = [
    { id: 1, name: 'Partner A', contact: 'Marek Z.', status: 'Aktywny' },
    { id: 2, name: 'Partner B', contact: 'Ewa Y.', status: 'Aktywny' },
];

export default function AdminPartners() {
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography variant="h4" gutterBottom>Partnerzy</Typography>
            <DataGrid rows={rows} columns={columns} checkboxSelection />
        </Box>
    );
}
