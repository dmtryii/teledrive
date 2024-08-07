import React from 'react';
import { Container, Typography, Link, Box } from '@mui/material';

const AboutPage = () => {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h4" gutterBottom>
          Help & Resources
        </Typography>
        <Typography variant="body1" gutterBottom>
        File Storage Platform Using Telegram API
        Our innovative file storage platform leverages the power of the Telegram API to offer unlimited file management capabilities. 
        Designed for flexibility and ease of use, it allows users to fully manipulate files and their structure.
        </Typography>
        <Box my={2}>
          <Link href="https://github.com/dmtryii/teledrive" target="_blank" rel="noopener">
            GitHub Repository
          </Link>
        </Box>
        <Box my={2}>
          <Link href="https://t.me/dmtryii" target="_blank" rel="noopener">
            Owner's Page (FQA)
          </Link>
        </Box>
      </Box>
    </Container>
  );
};

export default AboutPage;
