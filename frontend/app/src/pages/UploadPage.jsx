import React, { useState } from 'react';
import { Typography, Box, Card, CardContent} from '@mui/material';
import axiosInstance from '../config/axiosConfig';
import FileUploadForm from '../components/forms/FileUploadForm';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

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
            Upload File
          </Typography>
          <FileUploadForm
            handleFileChange={handleFileChange}
            file={file}
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