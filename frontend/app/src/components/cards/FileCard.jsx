import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, CardActions, FormControl, InputLabel, Select, MenuItem, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { CloudDownload as CloudDownloadIcon, Delete as DeleteIcon, DriveFileMove as MoveIcon } from '@mui/icons-material';
import truncateMiddle from '../../utils/stringUtils';
import fileFieldsUtils from '../../utils/fileFieldsUtils';
import axiosInstance from '../../config/axiosConfig';
import constructPath from '../../utils/folderUtils';

const FileCard = ({ file, allFolders, folderContents, setFolderContents, setMessage }) => {
  const [targetFolder, setTargetFolder] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [currentPath, setCurrentPath] = useState('');

  const fileName = file.document_info.file_name || 'Unknown File';
  const truncatedFileName = truncateMiddle(fileName, 20);

  const handleMove = () => {
    if (targetFolder) {
      handleMoveFile(file.id, targetFolder);
      setDialogOpen(false);
    }
  };

  const handleDownload = async (fileId) => {
    try {
      const response = await axiosInstance.get(`files/${fileId}/download`);
      window.open(response.data.file_url, '_blank');
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    }
  };

  const handleDelete = async (fileId) => {
    if (window.confirm('Are you sure you want to delete this file?')) {
      try {
        await axiosInstance.delete(`files/${fileId}`);
        setFolderContents(folderContents.map(folder => ({
          ...folder,
          files: folder.files.filter(file => file.id !== fileId),
          subfolders: folder.subfolders.map(subfolder => ({
            ...subfolder,
            files: subfolder.files.filter(file => file.id !== fileId)
          }))
        })));
        setMessage('File deleted successfully.');
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.message || error.message}`);
      }
    }
  };

  const handleMoveFile = async (fileId, targetFolderId) => {
    try {
      const response = await axiosInstance.post(`files/${fileId}/move`, { folder_id: targetFolderId });
      setFolderContents(folderContents.map(folder => {
        if (folder.id === targetFolderId) {
          return {
            ...folder,
            files: [...folder.files, response.data]
          };
        } else {
          return {
            ...folder,
            files: folder.files.filter(file => file.id !== fileId)
          };
        }
      }));
      setMessage('File moved successfully.');
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    }
  };

  const getCurrentPath = () => {
    const currentFolder = allFolders.find(folder => folder.id === file.folder_id);
    if (currentFolder) {
      return constructPath(currentFolder, allFolders);
    }
    return '';
  };

  const openMoveDialog = () => {
    setCurrentPath(getCurrentPath());
    setDialogOpen(true);
  };

  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Typography
          variant="h6"
          component="div"
          sx={{
            wordWrap: 'break-word',
            wordBreak: 'break-all',
            overflow: 'hidden',
            textOverflow: 'ellipsis'
          }}
        >
          {truncatedFileName}
        </Typography>
        <Typography color="textSecondary">
          Size: {fileFieldsUtils.formatFileSize(file.document_info.file_size)} MB
        </Typography>
        <Typography color="textSecondary" gutterBottom>
          Upload date: {fileFieldsUtils.formatTimestamp(file.upload)}
        </Typography>
      </CardContent>
      <CardActions style={{ justifyContent: 'space-between' }}>
        <Button
          color="primary"
          onClick={() => handleDownload(file.id)}
        >
          <CloudDownloadIcon />
        </Button>
        <Button
          color="secondary"
          onClick={() => handleDelete(file.id)}
        >
          <DeleteIcon />
        </Button>
        <Button
          onClick={openMoveDialog}
        >
          <MoveIcon />
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
          <Typography variant="body2" sx={{ mb: 2 }}>
            Name: {fileName}
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Current Path: {currentPath}
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Move to Folder</InputLabel>
            <Select
              value={targetFolder}
              onChange={(e) => setTargetFolder(e.target.value)}
            >
              {allFolders.map(folder => (
                <MenuItem key={folder.id} value={folder.id}>
                  {constructPath(folder, allFolders)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleMove} startIcon={<MoveIcon />}>
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

export default FileCard;
