import React, { useEffect, useState, Suspense } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Sidebar from './Sidebar';
import LoginForm from './login';
import { fetchScreens } from './api';

// Lazy load with error boundary
const SupportTicketsApp = React.lazy(() => 
  import('supportTicketsApp/App').catch(() => {
    console.error('Failed to load Support Tickets App');
    return { default: () => <div>Support Tickets App is not available</div> };
  })
);

const App = () => {
  const [screens, setScreens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
      loadScreensData();
    } else {
      setLoading(false);
    }
  }, []);

  const loadScreensData = async () => {
    try {
      const data = await fetchScreens();
      setScreens(data);
    } catch (error) {
      console.error('Error fetching screens:', error);
      if (error.response?.status === 401) {
        handleLogout();
        return;
      }
      setError('Failed to load screens');
      // Fallback to default screens
      setScreens([
        { tenant: 'Support Tickets', screenUrl: '/support' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (token) => {
    setIsAuthenticated(true);
    setLoading(true);
    loadScreensData();
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setScreens([]);
    window.location.reload();
  };

  if (!isAuthenticated) {
    return <LoginForm onLogin={handleLogin} />;
  }

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        Loading application...
      </div>
    );
  }

  return (
    <Router>
      <div style={{ display: 'flex', height: '100vh' }}>
        <Sidebar screens={screens} onLogout={handleLogout} />
        <div style={{ flex: 1, padding: '20px' }}>
          {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
          <Suspense fallback={<div>Loading module...</div>}>
            <Switch>
              <Route path="/support" component={SupportTicketsApp} />
              {screens.map(screen => (
                <Route key={screen.screenUrl} path={screen.screenUrl} component={SupportTicketsApp} />
              ))}
              <Route path="/" exact>
                <div>
                  <h1>Welcome to Flowbit Multitenant App</h1>
                  <p>Select a screen from the sidebar to get started.</p>
                </div>
              </Route>
            </Switch>
          </Suspense>
        </div>
      </div>
    </Router>
  );
};

export default App;