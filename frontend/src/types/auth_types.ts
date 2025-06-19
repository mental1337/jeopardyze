// Request types
export interface LoginRequest {
    username_or_email: string;
    password: string;
}

export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
    guest_id?: string;
}

export interface VerifyEmailRequest {
    email: string;
    code: string;
}

// Response types
export interface LoginResponse {
    access_token: string;
    token_type: string;
    user_id: number;
    username: string;
    email: string;
}

export interface RegisterResponse {
    message: string;
    email: string;
}

export interface VerifyEmailResponse {
    access_token: string;
    token_type: string;
    user_id: number;
    username: string;
    email: string;
}

export interface GuestResponse {
    access_token: string;
} 