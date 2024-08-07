import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  CardActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle
} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import DriveFileMoveIcon from '@mui/icons-material/DriveFileMove';
import axiosInstance from '../../config/axiosConfig';
import constructPath from '../../utils/folderUtils';

const FolderCard = ({ folder, onClick, folderContents, setFolderContents, setMessage }) => {
  const [targetFolder, setTargetFolder] = useState('');
  const [availableFolders, setAvailableFolders] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleMove = () => {
    if (targetFolder) {
      handleMoveFolder(folder.id, targetFolder);
      setDialogOpen(false);
    }
  };

  useEffect(() => {
    const fetchAvailableFolders = async () => {
      try {
        const response = await axiosInstance.get(`/folders/${folder.id}/available_to_move`);
        const folders = response.data;

        const foldersWithPath = folders.map(f => ({
          ...f,
          absolutePath: constructPath(f, folders)
        }));

        setAvailableFolders(foldersWithPath);
      } catch (error) {
        console.error('Error fetching folders:', error);
      }
    };

    fetchAvailableFolders();
  }, [folder.id]);

  const handleDelete = async (folderId) => {
    if (window.confirm('Are you sure you want to delete this folder? This will delete all its contents.')) {
      try {
        await axiosInstance.delete(`/folders/${folderId}`);
        setFolderContents(folderContents.map(folder => ({
          ...folder,
          files: folder.files.filter(file => !file.folderId || file.folderId !== folderId),
          subfolders: folder.subfolders
            .filter(subfolder => subfolder.id !== folderId)
            .map(subfolder => ({
              ...subfolder,
              files: subfolder.files.filter(file => file.folderId !== folderId),
              subfolders: subfolder.subfolders.filter(subSubfolder => subSubfolder.id !== folderId)
            }))
        })));
        setMessage('Folder deleted successfully.');
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.message || error.message}`);
      }
    }
  };

  const handleMoveFolder = async (folderId, targetFolderId) => {
    try {
      const response = await axiosInstance.post(`/folders/${folderId}/move`, {
        destination_folder_id: targetFolderId
      });
      setFolderContents(folderContents.map(folder => {
        if (folder.id === targetFolderId) {
          return {
            ...folder,
            subfolders: [...folder.subfolders, response.data]
          };
        } else {
          return {
            ...folder,
            subfolders: folder.subfolders.filter(subfolder => subfolder.id !== folderId)
          };
        }
      }));
      setMessage('Folder moved successfully.');
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    }
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" flexDirection="column" alignItems="center">
          <FolderIcon onClick={onClick} sx={{ cursor: 'pointer', fontSize: 60 }} />
          <Typography variant="h6" component="h3" sx={{ mt: 1 }}>
            {folder.name}
          </Typography>
        </Box>
      </CardContent>

      <CardActions style={{ justifyContent: 'space-between' }}>
        <Button onClick={() => setDialogOpen(true)}>
          <DriveFileMoveIcon />
        </Button>
        <Button color="secondary" onClick={() => handleDelete(folder.id)}>
          <DeleteIcon />
        </Button>
      </CardActions>

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
        sx={{ '& .MuiDialog-paper': { height: '400px' } }}
      >
        <DialogTitle>Move to Folder</DialogTitle>
        <DialogContent>
          <FormControl fullWidth>
            <InputLabel>Move to Folder</InputLabel>
            <Select
              value={targetFolder}
              onChange={(e) => setTargetFolder(e.target.value)}
            >
              {availableFolders.map(target => (
                <MenuItem key={target.id} value={target.id}>
                  {target.absolutePath}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleMove} startIcon={<DriveFileMoveIcon />}>
            Move
          </Button>
          <Button onClick={() => setDialogOpen(false)}>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default FolderCard;
