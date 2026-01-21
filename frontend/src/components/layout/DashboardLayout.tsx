'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function DashboardLayout({ children, role = 'admin' }: { children: React.ReactNode, role?: 'admin' | 'partner' }) {
    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <Topbar />
            <Sidebar role={role} />
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Toolbar />
                {children}
            </Box>
        </Box>
    );
}
