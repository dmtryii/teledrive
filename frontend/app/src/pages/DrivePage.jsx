import React, { useEffect, useState } from 'react';
import { Box, Typography, Container, Grid, CircularProgress, FormControl, InputLabel, Select, MenuItem, TextField } from '@mui/material';
import axiosInstance from '../config/axiosConfig';
import FileCard from '../components/cards/FileCard';
import fileSortUtils from '../utils/fileSortUtils';

const DrivePage = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [sortCriteria, setSortCriteria] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [searchQuery, setSearchQuery] = useState('');

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

  const handleSortChange = (event) => {
    setSortCriteria(event.target.value);
  };

  const handleOrderChange = (event) => {
    setSortOrder(event.target.value);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const filteredFiles = fileSortUtils.filterFiles(files, searchQuery);
  const sortedFiles = fileSortUtils.sortFiles(filteredFiles, sortCriteria, sortOrder);

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Files
        </Typography>
        <Grid container spacing={3} alignItems="center" mb={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              label="Search"
              variant="outlined"
              fullWidth
              value={searchQuery}
              onChange={handleSearchChange}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Sort By</InputLabel>
              <Select value={sortCriteria} onChange={handleSortChange}>
                <MenuItem value="name">Name</MenuItem>
                <MenuItem value="size">Size</MenuItem>
                <MenuItem value="upload">Upload Date</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Order</InputLabel>
              <Select value={sortOrder} onChange={handleOrderChange}>
                <MenuItem value="asc">Ascending</MenuItem>
                <MenuItem value="desc">Descending</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
            <CircularProgress />
          </Box>
        ) : (
          <Box mt={4}>
            {sortedFiles.length > 0 ? (
              <Grid container spacing={3}>
                {sortedFiles.map(file => (
                  <Grid item xs={12} sm={6} md={4} lg={3} key={file.id}>
                    <FileCard
                      file={file}
                      onDownload={handleDownload}
                      onDelete={handleDelete}
                    />
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
                <Typography>No files found.</Typography>
              </Box>
            )}
          </Box>
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
