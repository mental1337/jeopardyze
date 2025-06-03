import { Box, Button, FormControl, Input, HStack, useToast } from "@chakra-ui/react";
import { useState } from "react";

interface SignupBarProps {
    onClose: () => void;
}

export default function SignupBar({ onClose }: SignupBarProps) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const toast = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // TODO: Implement actual signup logic
            const response = await fetch("http://localhost:8000/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username,
                    email,
                    password,
                }),
            });

            if (!response.ok) {
                throw new Error("Signup failed");
            }

            const data = await response.json();
            // TODO: Handle email verification
            onClose();
            toast({
                title: "Success",
                description: "Please check your email for verification code",
                status: "success",
                duration: 5000,
                isClosable: true,
            });
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to sign up. Please try again.",
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