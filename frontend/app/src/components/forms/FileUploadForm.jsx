import { Button, Typography, Box, CircularProgress } from '@mui/material';
import truncateMiddle from '../../utils/stringUtils';

const FileUploadForm = ({ handleFileChange, files, handleSubmit, loading }) => (
  <form onSubmit={handleSubmit}>
      <Box mb={3} display="flex" justifyContent="center" alignItems="center">
        <input
          type="file"
          id="file-upload"
          onChange={handleFileChange}
          accept="*/*"
          multiple
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload">
          <Button variant="outlined" component="span">
            Choose Files
          </Button>
        </label>
        {files.length > 0 && (
          <Box ml={2}>
            {files.map((file, index) => (
              <Typography key={index} variant="body1" color="textPrimary">
                {truncateMiddle(file.name, 30)}
              </Typography>
            ))}
          </Box>
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
