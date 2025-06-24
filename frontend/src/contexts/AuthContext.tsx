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
    setPlayer: (player: Player | null) => void;
    handleLoginSuccess: (response: LoginResponse) => void;
    handleVerifyEmailSuccess: (response: VerifyEmailResponse) => void;
    handleGuestSuccess: (response: GuestResponse) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [player, setPlayer] = useState<Player | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const hasInitialized = useRef(false);

    // Function to create a guest session
    const createGuestSession = async () => {
        try {
            console.log("Creating guest session by calling /auth/guest");
            const { data } = await api.post<GuestResponse>('/auth/guest');
            const guestToken = data.access_token;
            setToken(guestToken);
            setPlayer({
                id: data.player_id,
                player_type: 'guest',
                display_name: data.display_name
            });
            
            localStorage.setItem('token', guestToken);
            return guestToken;
        } catch (error) {
            console.error('Failed to create guest session:', error);
            throw error;
        }
    };

    // Function to handle successful login
    const handleLoginSuccess = (response: LoginResponse) => {
        setToken(response.access_token);
        setPlayer({
            id: response.player_id,
            player_type: 'user',
            display_name: response.display_name
        });
        localStorage.setItem('token', response.access_token);
    };

    // Function to handle successful email verification
    const handleVerifyEmailSuccess = (response: VerifyEmailResponse) => {
        setToken(response.access_token);
        setPlayer({
            id: response.player_id,
            player_type: 'user',
            display_name: response.display_name
        });
        localStorage.setItem('token', response.access_token);
    };

    // Function to handle successful guest creation
    const handleGuestSuccess = (response: GuestResponse) => {
        setToken(response.access_token);
        setPlayer({
            id: response.player_id,
            player_type: 'guest',
            display_name: response.display_name
        });
        localStorage.setItem('token', response.access_token);
    };

    // Function to validate and parse token
    const validateToken = (token: string) => {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (payload.player_id && payload.player_type && payload.display_name) {
                setPlayer({
                    id: parseInt(payload.player_id),
                    player_type: payload.player_type,
                    display_name: payload.display_name
                });
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error parsing token:', error);
            return false;
        }
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
                // Token exists, validate it
                const isValid = validateToken(token);
                if (!isValid) {
                    // Invalid token, remove it and create guest session
                    localStorage.removeItem('token');
                    setToken(null);
                    setPlayer(null);
                    await createGuestSession();
                }
            } else {
                // No token exists, create a guest session
                await createGuestSession();
            }
            
            setIsLoading(false);
        };

        initializeAuth();
    }, []); // Only run on mount

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
            setPlayer(null);
        }
    }, [token]);

    // Listen for user token expiration events from axios interceptor
    useEffect(() => {
        const handleUserTokenExpired = () => {
            console.log('AuthContext: User token expired, updating state');
            setToken(null);
            setPlayer(null);
        };

        window.addEventListener('userTokenExpired', handleUserTokenExpired);
        
        return () => {
            window.removeEventListener('userTokenExpired', handleUserTokenExpired);
        };
    }, []);

    const logout = async () => {
        // Clear current player data
        setToken(null);
        setPlayer(null);
        localStorage.removeItem('token');

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
            setPlayer,
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