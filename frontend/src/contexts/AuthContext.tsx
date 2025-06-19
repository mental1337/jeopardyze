import { LoginResponse, GuestResponse, VerifyEmailResponse } from '../types/auth_types';
import { createContext, useContext, useState, useEffect, ReactNode, useRef } from 'react';
import api from '../lib/axios';

interface User {
    id: number;
    username: string;
    email: string;
}

interface AuthContextType {
    token: string | null;
    user: User | null;
    isGuest: boolean;
    guestId: number | null;
    isLoading: boolean;
    setToken: (token: string | null) => void;
    setUser: (user: User | null) => void;
    setIsGuest: (isGuest: boolean) => void;
    setGuestId: (guestId: number | null) => void;
    handleLoginSuccess: (response: LoginResponse) => void;
    handleVerifyEmailSuccess: (response: VerifyEmailResponse) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [user, setUser] = useState<User | null>(null);
    const [isGuest, setIsGuest] = useState<boolean>(false);
    const [guestId, setGuestId] = useState<number | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const hasInitialized = useRef(false);

    // Function to create a guest session
    const createGuestSession = async () => {
        try {
            console.log("Creating guest session by calling /auth/guest-session");
            const { data } = await api.post<GuestResponse>('/auth/guest-session');
            const guestToken = data.access_token;
            setToken(guestToken);
            setIsGuest(true);
            setUser(null);
            
            // Extract guest ID from the token
            const payload = JSON.parse(atob(guestToken.split('.')[1]));
            setGuestId(parseInt(payload.guest_id));
            
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
        setUser({
            id: response.user_id,
            username: response.username,
            email: response.email
        });
        setIsGuest(false);
        setGuestId(null);
        localStorage.setItem('token', response.access_token);
    };

    // Function to handle successful email verification
    const handleVerifyEmailSuccess = (response: VerifyEmailResponse) => {
        setToken(response.access_token);
        setUser({
            id: response.user_id,
            username: response.username,
            email: response.email
        });
        setIsGuest(false);
        setGuestId(null);
        localStorage.setItem('token', response.access_token);
    };

    // Function to validate and parse token
    const validateToken = (token: string) => {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (payload.sub === 'guest') {
                setIsGuest(true);
                setUser(null);
                setGuestId(parseInt(payload.guest_id));
            } else {
                // This is a user token - extract user info from the token
                setIsGuest(false);
                setGuestId(null);
                setUser({
                    id: parseInt(payload.sub),
                    username: payload.username,
                    email: payload.email
                });
            }
            return true;
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
                    setGuestId(null);
                    setUser(null);
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
            setIsGuest(false);
            setUser(null);
            setGuestId(null);
        }
    }, [token]);

    const logout = () => {
        setToken(null);
        setUser(null);
        setIsGuest(false);
        setGuestId(null);
        localStorage.removeItem('token');
    };

    return (
        <AuthContext.Provider value={{
            token,
            user,
            isGuest,
            guestId,
            isLoading,
            setToken,
            setUser,
            setIsGuest,
            setGuestId,
            handleLoginSuccess,
            handleVerifyEmailSuccess,
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