// Simple test for token parsing functionality
// This can be run with: npx vitest run tokenUtils.test.ts

import { describe, it, expect } from 'vitest';

// Mock JWT token structure
const createMockToken = (payload: any): string => {
    const header = { alg: 'HS256', typ: 'JWT' };
    const encodedHeader = btoa(JSON.stringify(header));
    const encodedPayload = btoa(JSON.stringify(payload));
    const signature = 'mock_signature';
    return `${encodedHeader}.${encodedPayload}.${signature}`;
};

// Token parsing function (copied from AuthContext)
const parsePlayerFromToken = (token: string): any => {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.player_id && payload.player_type && payload.display_name) {
            return {
                id: parseInt(payload.player_id),
                player_type: payload.player_type,
                display_name: payload.display_name
            };
        }
        return null;
    } catch (error) {
        console.error('Error parsing token:', error);
        return null;
    }
};

describe('Token Parsing', () => {
    it('should parse valid user token correctly', () => {
        const mockPayload = {
            player_id: '123',
            player_type: 'user',
            display_name: 'TestUser',
            exp: Date.now() + 3600000
        };
        
        const token = createMockToken(mockPayload);
        const result = parsePlayerFromToken(token);
        
        expect(result).toEqual({
            id: 123,
            player_type: 'user',
            display_name: 'TestUser'
        });
    });

    it('should parse valid guest token correctly', () => {
        const mockPayload = {
            player_id: '456',
            player_type: 'guest',
            display_name: 'Guest_abc123',
            exp: Date.now() + 3600000
        };
        
        const token = createMockToken(mockPayload);
        const result = parsePlayerFromToken(token);
        
        expect(result).toEqual({
            id: 456,
            player_type: 'guest',
            display_name: 'Guest_abc123'
        });
    });

    it('should return null for invalid token', () => {
        const result = parsePlayerFromToken('invalid.token.here');
        expect(result).toBeNull();
    });

    it('should return null for token with missing fields', () => {
        const mockPayload = {
            player_id: '123',
            // missing player_type and display_name
            exp: Date.now() + 3600000
        };
        
        const token = createMockToken(mockPayload);
        const result = parsePlayerFromToken(token);
        
        expect(result).toBeNull();
    });
}); 