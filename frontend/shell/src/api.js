import axios from "axios";

// Fix the process.env issue
const API_BASE_URL =
  typeof process !== "undefined" &&
  process.env &&
  process.env.REACT_APP_API_BASE_URL
    ? process.env.REACT_APP_API_BASE_URL
    : "http://localhost:8000";

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor for auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export const fetchScreens = async () => {
  const response = await apiClient.get("/me/screens");
  return response.data;
};

export const createTicket = async (ticketData) => {
  const response = await apiClient.post("/api/tickets", ticketData);
  return response.data;
};

export const updateTicketStatus = async (ticketId, status) => {
  const response = await apiClient.patch(`/api/tickets/${ticketId}`, {
    status,
  });
  return response.data;
};
