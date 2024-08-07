import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5001/api',
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const { response } = error;

    if (response && response.status === 401) {
      const currentPath = window.location.pathname;
      if (currentPath !== '/signin') {
        localStorage.removeItem('access_token');
        window.location = '/signin';
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
