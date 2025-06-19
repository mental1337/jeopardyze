import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor to handle token expiration
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        // If we get a 401 and haven't already tried to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            // Check if this is a guest token
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    if (payload.sub === 'guest') {
                        // Guest token expired - create new guest session
                        console.log('Guest token expired, creating new guest session');
                        const { data } = await api.post('/auth/guest-session');
                        const newToken = data.access_token;
                        
                        // Update localStorage
                        localStorage.setItem('token', newToken);
                        
                        // Update the original request with new token
                        originalRequest.headers.Authorization = `Bearer ${newToken}`;
                        
                        // Retry the original request
                        return api(originalRequest);
                    } else {
                        // User token expired - dispatch event to show login modal
                        console.log('User token expired, showing login modal');
                        localStorage.removeItem('token');
                        
                        // Dispatch custom event to trigger login modal
                        window.dispatchEvent(new CustomEvent('userTokenExpired'));
                        
                        return Promise.reject(error);
                    }
                } catch (parseError) {
                    console.error('Error parsing token:', parseError);
                    // If we can't parse the token, remove it and dispatch login event
                    localStorage.removeItem('token');
                    window.dispatchEvent(new CustomEvent('userTokenExpired'));
                    return Promise.reject(error);
                }
            }
        }
        
        return Promise.reject(error);
    }
);

export default api; 