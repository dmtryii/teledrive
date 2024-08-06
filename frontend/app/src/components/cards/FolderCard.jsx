import React, { useState, useEffect } from 'react';
import { Card, CardActionArea, CardContent, Typography, Box, IconButton, FormControl, InputLabel, Select, CardActions, MenuItem, Button } from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import DriveFileMoveIcon from '@mui/icons-material/DriveFileMove';
import axiosInstance from '../../config/axiosConfig';

const FolderCard = ({ folder, onClick, onDelete, onMove }) => {
  const [targetFolder, setTargetFolder] = useState('');
  const [folders, setFolders] = useState([]);

  useEffect(() => {
    const fetchAvailableFolders = async () => {
      try {
        const response = await axiosInstance.get(`/folders/${folder.id}/available_to_move`);
        setFolders(response.data);
      } catch (error) {
        console.error('Error fetching folders:', error);
      }
    };

    fetchAvailableFolders();
  }, [folder.id]);

  const handleMove = () => {
    if (targetFolder) {
      onMove(folder.id, targetFolder);
    }
  };

  return (
    <Card>
      <CardActionArea>
        <CardContent>
          <Box onClick={onClick} display="flex" alignItems="center">
            <FolderIcon sx={{ fontSize: 40, mr: 2 }} />
            <Typography variant="h6" component="h3">
              {folder.name}
            </Typography>
            <IconButton
              onClick={(event) => {
                event.stopPropagation();
                onDelete(folder.id);
              }}
              color="secondary"
              sx={{ ml: 'auto' }}
            >
              <DeleteIcon />
            </IconButton>
          </Box>
        </CardContent>
        <CardActions>
          <FormControl fullWidth>
            <InputLabel>Move to Folder</InputLabel>
            <Select
              value={targetFolder}
              onChange={(e) => setTargetFolder(e.target.value)}
              startIcon={<DriveFileMoveIcon />}
            >
              {folders.map(target => (
                <MenuItem key={target.id} value={target.id}>
                  {target.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            size="small"
            onClick={(event) => {
              event.stopPropagation();
              handleMove();
            }}
            startIcon={<DriveFileMoveIcon />}
          >
            Move
          </Button>
        </CardActions>
      </CardActionArea>
    </Card>
  );
};

export default FolderCard;
