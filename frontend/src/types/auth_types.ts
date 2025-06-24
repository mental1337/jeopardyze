// Request types
export interface LoginRequest {
    username_or_email: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
}


export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
    guest_id?: string;
}

export type RegisterResponse = LoginResponse

export interface VerifyEmailRequest {
    email: string;
    code: string;
}


export interface VerifyEmailResponse {
    message: string;
    access_token: string;
}

export interface GuestResponse {
    access_token: string;
} 