'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Klient', width: 200 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'status', headerName: 'Status', width: 130 },
    { field: 'date', headerName: 'Data', width: 130 },
];

const rows = [
    { id: 1, name: 'Jan Kowalski', email: 'jan@example.com', status: 'Nowy', date: '2023-11-01' },
    { id: 2, name: 'Anna Nowak', email: 'anna@example.com', status: 'W trakcie', date: '2023-11-02' },
];

export default function AdminLeads() {
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography variant="h4" gutterBottom>Wszystkie Leady</Typography>
            <DataGrid rows={rows} columns={columns} checkboxSelection />
        </Box>
    );
}
