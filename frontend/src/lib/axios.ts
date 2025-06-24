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
        if (error.response?.status === 401 &&
            error.response?.data?.detail === "Invalid authentication token" &&
            !originalRequest._retry) {
            originalRequest._retry = true;
            
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    if (payload.player_type === 'guest') {
                        // Guest token expired - create new guest session
                        console.log('Guest token expired, creating new guest session');
                        const { data } = await api.post('/auth/guest');
                        const newToken = data.access_token;
                        
                        // Dispatch event to notify AuthContext of token update
                        window.dispatchEvent(new CustomEvent('tokenUpdated', { 
                            detail: { token: newToken } 
                        }));
                        
                        // Update the original request with new token
                        originalRequest.headers.Authorization = `Bearer ${newToken}`;
                        
                        // Retry the original request
                        return api(originalRequest);
                    } else {
                        // User token expired - dispatch event to show login modal
                        console.log('User token expired, showing login modal');
                        
                        // Dispatch custom event to trigger login modal
                        window.dispatchEvent(new CustomEvent('userTokenExpired'));
                        
                        return Promise.reject(error);
                    }
                } catch (parseError) {
                    console.error('Error parsing token:', parseError);
                    // If we can't parse the token, dispatch login event
                    window.dispatchEvent(new CustomEvent('userTokenExpired'));
                    return Promise.reject(error);
                }
            }
            else {
                // We don't have a token, so we need to create a guest session
                console.log('No token found, creating guest session');
                const { data } = await api.post('/auth/guest');
                const newToken = data.access_token;
                window.dispatchEvent(new CustomEvent('tokenUpdated', { 
                    detail: { token: newToken } 
                }));
                return api(originalRequest);
            }
        }
        
        return Promise.reject(error);
    }
);

export default api; 