import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import SignInPage from '../pages/SignInPage';
import ProtectedRoute from './ProtectedRoute';
import UploadPage from '../pages/UploadPage';
import MyDrivePage from '../pages/MainPage';
import NotFoundPage from '../pages/NotFoundPage';

const getAccessToken = () => localStorage.getItem('access_token');

const isAuthenticated = () => !!getAccessToken();

const router = createBrowserRouter([
  {
    path: '/signin',
    element: <SignInPage />
  },
  {
    element: <ProtectedRoute isAuthenticated={isAuthenticated} />,
    children: [
      {
        path: '/',
        element: <MyDrivePage />,
        index: true
      },
      {
        path: '/upload',
        element: <UploadPage />
      },
      {
        path: '*',
        element: <NotFoundPage />
      }
    ]
  },
]);

export default router;
