import { RouterProvider } from 'react-router-dom';

import router from './routes/Router';


let App = () => {
  return (
    <div>
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
