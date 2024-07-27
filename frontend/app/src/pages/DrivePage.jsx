import React, { useEffect, useState } from 'react';
import { Box, Typography, Container, Grid } from '@mui/material';
import axiosInstance from '../config/axiosConfig';
import FileCard from '../components/cards/FileCard';

const DrivePage = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axiosInstance.get('files/');
        setFiles(response.data);
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.msg || error.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  const handleDownload = async (fileId) => {
    try {
      const response = await axiosInstance.get(`files/${fileId}/download`);
      window.open(response.data.file_url, '_blank');
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.msg || error.message}`);
    }
  };

  const handleDelete = async (fileId) => {
    if (window.confirm('Are you sure you want to delete this file?')) {
      try {
        await axiosInstance.delete(`files/${fileId}`);
        setFiles(files.filter(file => file.id !== fileId));
        setMessage('File deleted successfully.');
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.msg || error.message}`);
      }
    }
  };

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Files
        </Typography>
        {loading ? (
          <Typography>Loading...</Typography>
        ) : (
          <Grid container spacing={3}>
            {files.length > 0 ? (
              files.map(file => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={file.id}>
                  <FileCard
                    file={file}
                    onDownload={handleDownload}
                    onDelete={handleDelete}
                  />
                </Grid>
              ))
            ) : (
              <Typography>No files found.</Typography>
            )}
          </Grid>
        )}
        {message && (
          <Typography variant="body2" color="textSecondary" mt={2}>
            {message}
          </Typography>
        )}
      </Box>
    </Container>
  );
};

export default DrivePage;
