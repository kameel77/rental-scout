'use client';
import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import CalculateIcon from '@mui/icons-material/Calculate';
import PeopleIcon from '@mui/icons-material/People';
import AssignmentIcon from '@mui/icons-material/Assignment';
import SettingsIcon from '@mui/icons-material/Settings';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const drawerWidth = 240;

const menuItems = {
    admin: [
        { text: 'Dashboard', icon: <DashboardIcon />, href: '/admin' },
        { text: 'Pojazdy', icon: <DirectionsCarIcon />, href: '/admin/vehicles' },
        { text: 'Kalkulator', icon: <CalculateIcon />, href: '/admin/calculator' },
        { text: 'Leady', icon: <AssignmentIcon />, href: '/admin/leads' },
        { text: 'Partnerzy', icon: <PeopleIcon />, href: '/admin/partners' },
    ],
    partner: [
        { text: 'Dashboard', icon: <DashboardIcon />, href: '/partner' },
        { text: 'Kalkulator', icon: <CalculateIcon />, href: '/partner/calculator' },
        { text: 'Moje Leady', icon: <AssignmentIcon />, href: '/partner/leads' },
    ],
};

export default function Sidebar({ role = 'admin' }: { role?: 'admin' | 'partner' }) {
    const pathname = usePathname();
    const items = menuItems[role];

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
            }}
        >
            <Box sx={{ overflow: 'auto' }}>
                <List>
                    {items.map((item) => (
                        <ListItem key={item.text} disablePadding>
                            <ListItemButton component={Link} href={item.href} selected={pathname === item.href}>
                                <ListItemIcon>
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText primary={item.text} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Box>
        </Drawer>
    );
}
