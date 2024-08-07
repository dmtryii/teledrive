import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Container,
  Grid,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Breadcrumbs,
  Link,
  Button
} from '@mui/material';
import axiosInstance from '../config/axiosConfig';
import FileCard from '../components/cards/FileCard';
import FolderCard from '../components/cards/FolderCard';
import fileSortUtils from '../utils/fileSortUtils';
import FolderCreationForm from '../components/forms/FolderCreationForm';

const DrivePage = () => {
  const [folderContents, setFolderContents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  const [sortCriteria, setSortCriteria] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [searchQuery, setSearchQuery] = useState('');

  const [path, setPath] = useState([]);
  const [allFolders, setAllFolders] = useState([]);

  const [showCreateFolderForm, setShowCreateFolderForm] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');

  useEffect(() => {
    const fetchFolders = async (folderId = '') => {
      setLoading(true);
      try {
        const response = await axiosInstance.get(`folders/${folderId}`);
        setFolderContents([response.data]);
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.message || error.message}`);
      } finally {
        setLoading(false);
      }
    };

    const fetchAllFolders = async () => {
      try {
        const response = await axiosInstance.get('folders/all');
        setAllFolders(response.data);
      } catch (error) {
        setMessage(`Error: ${error.response?.data?.message || error.message}`);
      }
    };

    fetchFolders();
    fetchAllFolders();
  }, []);

  const handleSortChange = (event) => {
    setSortCriteria(event.target.value);
  };

  const handleOrderChange = (event) => {
    setSortOrder(event.target.value);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleNewFolderNameChange = (event) => {
    setNewFolderName(event.target.value);
  };

  const handleFolderClick = async (folderId, folderName) => {
    setLoading(true);
    try {
      const response = await axiosInstance.get(`folders/${folderId}`);
      setFolderContents([response.data]);
      setPath(prevPath => [...prevPath, { id: folderId, name: folderName }]);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBreadcrumbClick = async (folderId, index) => {
    setLoading(true);
    try {
      const response = await axiosInstance.get(`folders/${folderId}`);
      setFolderContents([response.data]);
      setPath(path.slice(0, index + 1));
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFolder = async () => {
    try {
      const response = await axiosInstance.post('folders/', {
        name: newFolderName,
        parent_id: path.length ? path[path.length - 1].id : '',
      });
  
      const newFolder = response.data.new_folder;
  
      setFolderContents(prevFolders => {
        const addFolderRecursively = (folders) => {
          return folders.map(folder => {
            if (folder.id === newFolder.parent_id) {
              return {
                ...folder,
                subfolders: [newFolder, ...folder.subfolders],
              };
            }
            return {
              ...folder,
              subfolders: addFolderRecursively(folder.subfolders),
            };
          });
        };
  
        return addFolderRecursively(prevFolders);
      });
  
      setMessage('Folder created successfully.');
      setNewFolderName('');
      setShowCreateFolderForm(false);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || error.message}`);
    }
  };

  const renderFolders = (folder) => {
    const filteredFiles = fileSortUtils.filterFiles(folder.files, searchQuery);
    const sortedFiles = fileSortUtils.sortFiles(filteredFiles, sortCriteria, sortOrder);

    return (
      <Box key={folder.id} mt={4}>
        <Grid container spacing={3}>
          {sortedFiles.map(file => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={file.id}>
              <FileCard
                file={file}
                allFolders={allFolders}
                folderContents={folderContents}
                setFolderContents={setFolderContents}
                setMessage={setMessage}
              />
            </Grid>
          ))}
          {folder.subfolders.map(subfolder => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={subfolder.id}>
              <FolderCard
                folder={subfolder}
                onClick={() => handleFolderClick(subfolder.id, subfolder.name)}
                folderContents={folderContents}
                setFolderContents={setFolderContents}
                setMessage={setMessage}
              />
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Files
        </Typography>
      </Box>
      <Breadcrumbs aria-label="breadcrumb">
        <Link
          color="inherit"
          onClick={() => handleBreadcrumbClick('', -1)}
          style={{ cursor: 'pointer' }}
        >
          root
        </Link>
        {path.map((folder, index) => (
          <Link
            key={folder.id}
            color="inherit"
            onClick={() => handleBreadcrumbClick(folder.id, index)}
            style={{ cursor: 'pointer' }}
          >
            {folder.name}
          </Link>
        ))}
      </Breadcrumbs>

      <Box mt={4}>
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

        <Button
          variant="contained"
          color="primary"
          onClick={() => setShowCreateFolderForm(!showCreateFolderForm)}
          sx={{ mb: 2 }}
        >
          {showCreateFolderForm ? 'Cancel' : 'Create New Folder'}
        </Button>

        {showCreateFolderForm && (
          <FolderCreationForm
            newFolderName={newFolderName}
            onNameChange={handleNewFolderNameChange}
            onCreate={handleCreateFolder}
          />
        )}

        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
            <CircularProgress />
          </Box>
        ) : (
          folderContents.map(folder => renderFolders(folder))
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
