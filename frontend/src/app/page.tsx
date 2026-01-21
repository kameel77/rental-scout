'use client';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Link from 'next/link';
import Paper from '@mui/material/Paper';

export default function Home() {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        bgcolor: 'background.default',
      }}
    >
      <Paper sx={{ p: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Rental Scout
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Wybierz rolę aby kontynuować
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="contained" component={Link} href="/admin">
            Admin Dashboard
          </Button>
          <Button variant="outlined" component={Link} href="/partner">
            Partner Dashboard
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
