import { createRoot } from 'react-dom/client';
import './App.css';
import '@lynx-js/web-core/client';

const App = () => {
  return (
    <lynx-view
      style={{ height: '100vh', width: '100vw' }}
      url="/index.web.bundle"
    ></lynx-view>
  );
};

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
