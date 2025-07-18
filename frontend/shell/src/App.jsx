import React, { useEffect, useState, Suspense } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Sidebar from './Sidebar';
import LoginForm from './login';
import { fetchScreens } from './api';

// Better error boundary for Module Federation
const SupportTicketsApp = React.lazy(() => {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = 'http://localhost:3001/remoteEntry.js';
    script.onload = () => {
      // Give webpack time to register the remote
      setTimeout(() => {
        import('supportTicketsApp/App')
          .then(module => resolve(module))
          .catch(() => resolve({ 
            default: () => (
              <div style={{padding: '20px', textAlign: 'center'}}>
                <h2>Support Tickets App Unavailable</h2>
                <p>Please ensure the support tickets service is running on port 3001</p>
                <button onClick={() => window.location.reload()}>Retry</button>
              </div>
            )
          }));
      }, 100);
    };
    script.onerror = () => resolve({ 
      default: () => (
        <div style={{padding: '20px', textAlign: 'center'}}>
          <h2>Support Tickets App Unavailable</h2>
          <p>Please ensure the support tickets service is running on port 3001</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      )
    });
    document.head.appendChild(script);
  });
});

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
          <Suspense fallback={<div style={{padding: '20px'}}>Loading Support Tickets...</div>}>
            <Switch>
              <Route path="/support" component={SupportTicketsApp} />
              {screens.map(screen => (
                <Route key={screen.screenUrl} path={screen.screenUrl} component={SupportTicketsApp} />
              ))}
              <Route path="/" exact>
                <div>
                  <h1>Welcome to Flowbit Multitenant App</h1>
                  <p>Select a screen from the sidebar to get started.</p>
                  <div style={{marginTop: '20px'}}>
                    <h3>Available Screens:</h3>
                    <ul>
                      {screens.map(screen => (
                        <li key={screen.screenUrl}>
                          {screen.tenant} - {screen.screenUrl}
                        </li>
                      ))}
                    </ul>
                  </div>
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