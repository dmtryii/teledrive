import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import TopMenu from '../components/TopMenu';

const ProtectedRoute = ({ isAuthenticated }) => {

  if (!isAuthenticated()) {
    return <Navigate to="/signin" replace />;
  }

  return (
    <div>
      <TopMenu />
      <Outlet />
    </div>
  ) 
};

export default ProtectedRoute;