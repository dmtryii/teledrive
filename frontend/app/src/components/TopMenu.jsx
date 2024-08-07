import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const TopMenu = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          TeleDrive
        </Typography>
        <Button color="inherit" onClick={() => navigate('/')}>
          MyDrive
        </Button>
        <Button color="inherit" onClick={() => navigate('/upload')}>
          Upload
        </Button>
        <Button color="inherit" onClick={() => {
          navigate('/signin');
          localStorage.removeItem('access_token');
        }}>
          SignOut
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default TopMenu;
