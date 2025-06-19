import { useCallback } from 'react';
import { GuestResponse } from '../types/auth_types';
import { useAuth } from '../contexts/AuthContext';
import api from '../lib/axios';

export function useGuestSession() {
    const { setToken, setIsGuest } = useAuth();

    const createGuestSession = useCallback(async () => {
        try {
            const { data } = await api.post<GuestResponse>('/auth/guest-session');
            setToken(data.access_token);
            setIsGuest(true);
            return data.access_token;
        } catch (error) {
            console.error('Failed to create guest session:', error);
            throw error;
        }
    }, [setToken, setIsGuest]);

    return { createGuestSession };
} 