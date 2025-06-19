import { Box, Button, FormControl, Input, HStack, useToast } from "@chakra-ui/react";
import { useState } from "react";
import { RegisterRequest, RegisterResponse } from "../types/auth_types";
import axios from "axios";

interface SignupBarProps {
    onClose: () => void;
    onRegisterSuccess: (response: RegisterResponse) => void;
    guestId?: string;
}

export default function SignupBar({ onClose, onRegisterSuccess, guestId }: SignupBarProps) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const toast = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const request: RegisterRequest = {
                username,
                email,
                password,
                guest_id: guestId,
            };

            const { data } = await axios.post<RegisterResponse>(
                "http://localhost:8000/api/auth/register",
                request
            );

            onRegisterSuccess(data);
            onClose();
            toast({
                title: "Success",
                description: "Registration successful! Please check your email for verification.",
                status: "success",
                duration: 5000,
                isClosable: true,
            });
        } catch (error) {
            const errorMessage = axios.isAxiosError(error) && error.response?.data?.detail
                ? error.response.data.detail
                : "Failed to register. Please try again.";
            
            toast({
                title: "Error",
                description: errorMessage,
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box p={4} bg="gray.200" borderRadius={10} mt={2}>
            <form onSubmit={handleSubmit}>
                <HStack spacing={4}>
                    <FormControl isRequired>
                        <Input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Username"
                            size="sm"
                            bg="gray.100"
                        />
                    </FormControl>

                    <FormControl isRequired>
                        <Input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Email"
                            size="sm"
                            bg="gray.100"
                        />
                    </FormControl>

                    <FormControl isRequired>
                        <Input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Password"
                            size="sm"
                            bg="gray.100"
                        />
                    </FormControl>

                    <Button
                        type="submit"
                        colorScheme="blue"
                        isLoading={isLoading}
                        size="sm"
                        pl={6}
                        pr={6}
                    >
                        Sign Up
                    </Button>
                </HStack>
            </form>
        </Box>
    );
} 