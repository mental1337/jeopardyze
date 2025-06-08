import { createContext, useContext, useState, ReactNode } from 'react';
import { LoginResponse, GuestSessionResponse } from '../types/auth_types';

interface AuthContextType {
    token: string | null;
    isGuest: boolean;
    user: {
        id: number | null;
        username: string | null;
        email: string | null;
    } | null;
    setToken: (token: string | null) => void;
    setIsGuest: (isGuest: boolean) => void;
    setUser: (user: { id: number; username: string; email: string; } | null) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [isGuest, setIsGuest] = useState<boolean>(localStorage.getItem('isGuest') === 'true');
    const [user, setUser] = useState<{ id: number; username: string; email: string; } | null>(() => {
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const handleSetToken = (newToken: string | null) => {
        setToken(newToken);
        if (newToken) {
            localStorage.setItem('token', newToken);
        } else {
            localStorage.removeItem('token');
        }
    };

    const handleSetIsGuest = (newIsGuest: boolean) => {
        setIsGuest(newIsGuest);
        localStorage.setItem('isGuest', String(newIsGuest));
    };

    const handleSetUser = (newUser: { id: number; username: string; email: string; } | null) => {
        setUser(newUser);
        if (newUser) {
            localStorage.setItem('user', JSON.stringify(newUser));
        } else {
            localStorage.removeItem('user');
        }
    };

    const logout = () => {
        handleSetToken(null);
        handleSetIsGuest(false);
        handleSetUser(null);
    };

    return (
        <AuthContext.Provider value={{
            token,
            isGuest,
            user,
            setToken: handleSetToken,
            setIsGuest: handleSetIsGuest,
            setUser: handleSetUser,
            logout,
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