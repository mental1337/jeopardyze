import { useAuth } from '../contexts/AuthContext';
import api from '../lib/axios';
import { GuestSessionResponse } from '../types/auth_types';

export function useGuestSession() {
    const { setToken, setIsGuest } = useAuth();

    const createGuestSession = async () => {
        try {
            const { data } = await api.post<GuestSessionResponse>('/auth/guest-session');
            setToken(data.access_token);
            setIsGuest(true);
            return data.access_token;
        } catch (error) {
            console.error('Failed to create guest session:', error);
            throw error;
        }
    };

    return { createGuestSession };
} 