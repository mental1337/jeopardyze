import { LoginResponse, GuestResponse, VerifyEmailResponse } from '../types/auth_types';
import { createContext, useContext, useState, useEffect, ReactNode, useRef } from 'react';
import api from '../lib/axios';

interface Player {
    id: number;
    player_type: 'user' | 'guest';
    display_name: string;
}

interface AuthContextType {
    token: string | null;
    player: Player | null;
    isLoading: boolean;
    setToken: (token: string | null) => void;
    handleLoginSuccess: (response: LoginResponse) => void;
    handleVerifyEmailSuccess: (response: VerifyEmailResponse) => void;
    handleGuestSuccess: (response: GuestResponse) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper function to parse player data from JWT token
const parsePlayerFromToken = (token: string): Player | null => {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        console.log('Parsed token payload:', payload);
        if (payload.player_id && payload.player_type && payload.display_name) {
            const player = {
                id: parseInt(payload.player_id),
                player_type: payload.player_type,
                display_name: payload.display_name
            };
            console.log('Extracted player data:', player);
            return player;
        }
        console.log('Missing required fields in token payload');
        return null;
    } catch (error) {
        console.error('Error parsing token:', error);
        return null;
    }
};

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setTokenState] = useState<string | null>(localStorage.getItem('token'));
    const [player, setPlayer] = useState<Player | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const hasInitialized = useRef(false);

    // Function to set token and automatically update player data
    const setToken = (newToken: string | null) => {
        console.log('setToken called with:', newToken ? 'new token' : 'null');
        setTokenState(newToken);
        
        if (newToken) {
            const playerData = parsePlayerFromToken(newToken);
            console.log('Setting player data from token:', playerData);
            setPlayer(playerData);
            localStorage.setItem('token', newToken);
        } else {
            console.log('Clearing player data');
            setPlayer(null);
            localStorage.removeItem('token');
        }
    };

    // Function to create a guest session
    const createGuestSession = async () => {
        try {
            console.log("Creating guest session by calling /auth/guest");
            const { data } = await api.post<GuestResponse>('/auth/guest');
            setToken(data.access_token);
            return data.access_token;
        } catch (error) {
            console.error('Failed to create guest session:', error);
            throw error;
        }
    };

    // Function to handle successful login
    const handleLoginSuccess = (response: LoginResponse) => {
        setToken(response.access_token);
    };

    // Function to handle successful email verification
    const handleVerifyEmailSuccess = (response: VerifyEmailResponse) => {
        setToken(response.access_token);
    };

    // Function to handle successful guest creation
    const handleGuestSuccess = (response: GuestResponse) => {
        setToken(response.access_token);
    };

    useEffect(() => {
        const initializeAuth = async () => {
            // Prevent multiple initializations
            if (hasInitialized.current) {
                return;
            }
            
            hasInitialized.current = true;
            setIsLoading(true);
            
            if (token) {
                // Token exists, validate it by parsing
                const playerData = parsePlayerFromToken(token);
                if (!playerData) {
                    // Invalid token, remove it and create guest session
                    setToken(null);
                    await createGuestSession();
                } else {
                    // Valid token, set player data
                    setPlayer(playerData);
                }
            } else {
                // No token exists, create a guest session
                await createGuestSession();
            }
            
            setIsLoading(false);
        };

        initializeAuth();
    }, []); // Only run on mount

    // Update player data when token changes
    useEffect(() => {
        if (token) {
            const playerData = parsePlayerFromToken(token);
            setPlayer(playerData);
        } else {
            setPlayer(null);
        }
    }, [token]);

    // Listen for user token expiration events from axios interceptor
    useEffect(() => {
        const handleUserTokenExpired = () => {
            console.log('AuthContext: User token expired, updating state');
            setToken(null);
        };

        const handleTokenUpdated = (event: CustomEvent) => {
            console.log('AuthContext: Token updated by axios interceptor');
            setToken(event.detail.token);
        };

        window.addEventListener('userTokenExpired', handleUserTokenExpired);
        window.addEventListener('tokenUpdated', handleTokenUpdated as EventListener);
        
        return () => {
            window.removeEventListener('userTokenExpired', handleUserTokenExpired);
            window.removeEventListener('tokenUpdated', handleTokenUpdated as EventListener);
        };
    }, []);

    const logout = async () => {
        // Clear current player data
        setToken(null);

        // Create new guest session
        try {
            await createGuestSession();
        } catch (error) {
            console.error('Failed to create guest session after logout:', error);
        }
    };

    return (
        <AuthContext.Provider value={{
            token,
            player,
            isLoading,
            setToken,
            handleLoginSuccess,
            handleVerifyEmailSuccess,
            handleGuestSuccess,
            logout
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
} 