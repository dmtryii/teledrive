import React, { useState } from 'react';
import { Typography, Box, Card, CardContent } from '@mui/material';
import axiosInstance from '../config/axiosConfig';
import FileUploadForm from '../components/forms/FileUploadForm';

const UploadPage = () => {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (files.length === 0) {
      setMessage('Please select files to upload.');
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    setLoading(true);

    try {
      const response = await axiosInstance.post('files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.msg);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.msg || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="85vh"
      textAlign="center"
    >
      <Card sx={{ maxWidth: 500, width: '100%', p: 2, boxShadow: 3 }}>
        <CardContent>
          <Typography variant="h4" component="h1" gutterBottom>
            Upload Files
          </Typography>
          <FileUploadForm
            handleFileChange={handleFileChange}
            files={files}
            handleSubmit={handleSubmit}
            loading={loading}
          />
          {message && (
            <Typography variant="body2" color="textSecondary" mt={2}>
              {message}
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default UploadPage;
