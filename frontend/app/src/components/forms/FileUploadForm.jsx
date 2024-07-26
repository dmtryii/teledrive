import { Button, Typography, Box, CircularProgress } from '@mui/material';

const FileUploadForm = ({ handleFileChange, file, handleSubmit, loading }) => (
  <form onSubmit={handleSubmit}>
    <Box mb={3} display="flex" justifyContent="center" alignItems="center">
      <input
        type="file"
        id="file-upload"
        onChange={handleFileChange}
        accept="*/*"
        style={{ display: 'none' }}
      />
      <label htmlFor="file-upload">
        <Button variant="outlined" component="span">
          Choose File
        </Button>
      </label>
      {file && (
        <Typography variant="body1" color="textPrimary" ml={2}>
          {file.name}
        </Typography>
      )}
    </Box>
    {loading ? (
      <Box display="flex" justifyContent="center" mt={2}>
        <CircularProgress />
      </Box>
    ) : (
      <Box mt={2}>
        <Button variant="contained" color="primary" type="submit" fullWidth>
          Upload
        </Button>
      </Box>
    )}
  </form>
);

export default FileUploadForm;