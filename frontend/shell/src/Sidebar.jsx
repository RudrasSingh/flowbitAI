import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = ({ screens, onLogout }) => (
    <div style={{ 
        width: '250px', 
        background: '#f8f9fa', 
        padding: '20px',
        borderRight: '1px solid #dee2e6'
    }}>
        <h2 style={{ marginBottom: '30px' }}>Navigation</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
            {screens.map(screen => (
                <li key={screen.screenUrl} style={{ marginBottom: '10px' }}>
                    <Link 
                        to={screen.screenUrl}
                        style={{ 
                            display: 'block',
                            padding: '10px',
                            textDecoration: 'none',
                            color: '#333',
                            borderRadius: '4px',
                            backgroundColor: 'white',
                            border: '1px solid #ddd'
                        }}
                    >
                        {screen.tenant}
                    </Link>
                </li>
            ))}
        </ul>
        
        <button 
            onClick={onLogout}
            style={{
                marginTop: '20px',
                padding: '10px 20px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                width: '100%'
            }}
        >
            Logout
        </button>
    </div>
);

export default Sidebar;