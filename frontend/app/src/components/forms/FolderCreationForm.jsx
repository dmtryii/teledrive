import React from 'react';
import { Box, Typography, TextField, Button } from '@mui/material';

const FolderCreationForm = ({ newFolderName, onNameChange, onCreate }) => (
  <Box mt={4} mb={2}>
    <Typography variant="h6" component="h3">
      Create New Folder
    </Typography>
    <TextField
      label="Folder Name"
      variant="outlined"
      fullWidth
      value={newFolderName}
      onChange={onNameChange}
    />
    <Button
      variant="contained"
      color="primary"
      onClick={onCreate}
      disabled={!newFolderName.trim()}
      sx={{ mt: 2 }}
    >
      Create Folder
    </Button>
  </Box>
);

export default FolderCreationForm;
