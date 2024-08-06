import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, CardActions, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { CloudDownload as CloudDownloadIcon, Delete as DeleteIcon, DriveFileMove as MoveIcon } from '@mui/icons-material';
import truncateMiddle from '../../utils/stringUtils';
import fileFieldsUtils from '../../utils/fileFieldsUtils';

const FileCard = ({ file, onDownload, onDelete, onMove, folders }) => {
  const [targetFolder, setTargetFolder] = useState('');

  const handleMove = () => {
    if (targetFolder) {
      onMove(file.id, targetFolder);
    }
  };

  const fileName = file.document_info.file_name || 'Unknown File';
  const truncatedFileName = truncateMiddle(fileName, 20);

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
      <CardActions>
        <Button
          size="small"
          color="primary"
          onClick={() => onDownload(file.id)}
          startIcon={<CloudDownloadIcon />}
        >
          Download
        </Button>
        <Button
          size="small"
          color="secondary"
          onClick={() => onDelete(file.id)}
          startIcon={<DeleteIcon />}
        >
          Delete
        </Button>
      </CardActions>
      <CardActions>
        <FormControl fullWidth>
          <InputLabel>Move to Folder</InputLabel>
          <Select
            value={targetFolder}
            onChange={(e) => setTargetFolder(e.target.value)}
            startIcon={<MoveIcon />}
          >
            {folders.map(folder => (
              <MenuItem key={folder.id} value={folder.id}>
                {folder.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button
          size="small"
          onClick={handleMove}
          startIcon={<MoveIcon />}
        >
          Move
        </Button>
      </CardActions>
    </Card>
  );
};

export default FileCard;