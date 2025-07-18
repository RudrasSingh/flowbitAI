import React, { useEffect, useState } from 'react';
import { fetchTickets, createTicket } from './api';

const CreateTicketForm = ({ onTicketCreated, onCancel }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            await createTicket({ title, description });
            onTicketCreated();
            setTitle('');
            setDescription('');
        } catch (error) {
            console.error('Error creating ticket:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ 
            border: '1px solid #ddd', 
            padding: '20px', 
            marginBottom: '20px',
            borderRadius: '5px',
            backgroundColor: '#f9f9f9'
        }}>
            <h3>Create New Ticket</h3>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                        style={{ 
                            width: '100%', 
                            padding: '8px',
                            border: '1px solid #ccc',
                            borderRadius: '4px'
                        }}
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Description:</label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                        rows="4"
                        style={{ 
                            width: '100%', 
                            padding: '8px',
                            border: '1px solid #ccc',
                            borderRadius: '4px'
                        }}
                    />
                </div>
                <div>
                    <button 
                        type="submit" 
                        disabled={loading}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#28a745',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            marginRight: '10px',
                            cursor: 'pointer'
                        }}
                    >
                        {loading ? 'Creating...' : 'Create Ticket'}
                    </button>
                    <button 
                        type="button" 
                        onClick={onCancel}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#6c757d',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

const App = () => {
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showCreateForm, setShowCreateForm] = useState(false);

    const loadTickets = async () => {
        try {
            setError(null);
            const data = await fetchTickets();
            setTickets(Array.isArray(data) ? data : []);
        } catch (err) {
            console.error('Error fetching tickets:', err);
            setError(err.response?.status === 401 ? 'Please login to view tickets' : err.message);
            setTickets([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadTickets();
        const intervalId = setInterval(loadTickets, 10000);
        return () => clearInterval(intervalId);
    }, []);

    const handleTicketCreated = () => {
        setShowCreateForm(false);
        loadTickets();
    };

    if (loading) {
        return (
            <div style={{ padding: '20px', textAlign: 'center' }}>
                <div>Loading tickets...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: '20px', color: 'red' }}>
                <h2>Error</h2>
                <p>{error}</p>
                <button onClick={() => window.location.reload()}>
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h1>Support Tickets</h1>
                <button
                    onClick={() => setShowCreateForm(!showCreateForm)}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                >
                    {showCreateForm ? 'Cancel' : 'Create New Ticket'}
                </button>
            </div>

            {showCreateForm && (
                <CreateTicketForm 
                    onTicketCreated={handleTicketCreated}
                    onCancel={() => setShowCreateForm(false)}
                />
            )}

            {tickets.length === 0 ? (
                <div>
                    <p>No tickets found.</p>
                    <button onClick={() => window.location.reload()}>
                        Refresh
                    </button>
                </div>
            ) : (
                <div>
                    <p>Total tickets: {tickets.length}</p>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {tickets.map(ticket => (
                            <li key={ticket.id} style={{ 
                                border: '1px solid #ddd', 
                                margin: '10px 0', 
                                padding: '15px',
                                borderRadius: '5px',
                                backgroundColor: '#f9f9f9'
                            }}>
                                <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>
                                    {ticket.title}
                                </h3>
                                <p style={{ margin: '5px 0', color: '#666' }}>
                                    {ticket.description}
                                </p>
                                <div style={{ 
                                    display: 'flex', 
                                    justifyContent: 'space-between',
                                    fontSize: '0.9em',
                                    color: '#888'
                                }}>
                                    <span>Status: <strong>{ticket.status}</strong></span>
                                    <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default App;