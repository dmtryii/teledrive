import React from 'react';
import { Card, CardContent, Typography, Button, CardActions } from '@mui/material';
import { CloudDownload as CloudDownloadIcon, Delete as DeleteIcon } from '@mui/icons-material';

const truncateMiddle = (text, maxLength) => {
    if (text.length <= maxLength) return text;
    const halfLength = Math.floor(maxLength / 2);
    return `${text.slice(0, halfLength)}...${text.slice(-halfLength)}`;
};

const FileCard = ({ file, onDownload, onDelete }) => {

    const fileName = file.document_info.file_name || 'Unknown File';
    const truncatedFileName = truncateMiddle(fileName, 20);

    return (
        <Card sx={{ minWidth: 275, mb: 2 }}>
        <CardContent>
        <Typography
            variant="h6"
            component="div"
            sx={{ overflow: 'hidden', textOverflow: 'ellipsis' }}
            >
            {truncatedFileName}
            </Typography>
            <Typography color="textSecondary">
            File ID: {file.id}
            </Typography>
            <Typography color="textSecondary">
            File Size: {file.document_info.file_size} bytes
            </Typography>
        </CardContent>
        <CardActions>
            <Button
            size="small"
            color="primary"
            startIcon={<CloudDownloadIcon />}
            onClick={() => onDownload(file.id)}
            >
            Download
            </Button>
            <Button
            size="small"
            color="secondary"
            startIcon={<DeleteIcon />}
            onClick={() => onDelete(file.id)}
            >
            Delete
            </Button>
        </CardActions>
        </Card>
    );
};

export default FileCard;
