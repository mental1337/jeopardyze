import { LoginResponse, GuestResponse } from '../types/auth_types';
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
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
    setToken: (token: string | null) => void;
    setUser: (user: User | null) => void;
    setIsGuest: (isGuest: boolean) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [user, setUser] = useState<User | null>(null);
    const [isGuest, setIsGuest] = useState<boolean>(false);

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
            // Check if token is for a guest or user
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                if (payload.sub === 'guest') {
                    setIsGuest(true);
                    setUser(null);
                } else {
                    setIsGuest(false);
                    // For user tokens, you might want to fetch user info here
                    // or include it in the token payload
                    // TODO: fetch user info here
                }
            } catch (error) {
                console.error('Error parsing token:', error);
                setToken(null);
                setIsGuest(false);
            }
        } else {
            localStorage.removeItem('token');
            setIsGuest(false);
            setUser(null);
        }
    }, [token]);

    const logout = () => {
        setToken(null);
        setUser(null);
        setIsGuest(false);
        localStorage.removeItem('token');
    };

    return (
        <AuthContext.Provider value={{
            token,
            user,
            isGuest,
            setToken,
            setUser,
            setIsGuest,
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