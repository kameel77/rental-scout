'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Link from 'next/link';
import AddIcon from '@mui/icons-material/Add';

const columns: GridColDef[] = [
    { field: 'title', headerName: 'Nazwa', width: 200 },
    { field: 'make', headerName: 'Marka', width: 130 },
    { field: 'model', headerName: 'Model', width: 130 },
    { field: 'year', headerName: 'Rok', type: 'number', width: 90 },
    {
        field: 'status',
        headerName: 'Status',
        width: 120,
        valueGetter: (value, row) => row.is_published ? 'Opublikowany' : 'Roboczy',
    },
];

export default function VehicleList() {
    const [rows, setRows] = React.useState([]);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetch('http://localhost:8000/backoffice/vehicles-catalog')
            .then((res) => res.json())
            .then((data) => {
                setRows(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Failed to fetch vehicles', err);
                setLoading(false);
            });
    }, []);

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
                loading={loading}
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
