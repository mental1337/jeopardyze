import { Box, Button, FormControl, Input, HStack, useToast } from "@chakra-ui/react";
import { useState } from "react";

interface SigninBarProps {
    onClose: () => void;
}

export default function SigninBar({ onClose }: SigninBarProps) {
    const [usernameOrEmail, setUsernameOrEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const toast = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // TODO: Implement actual signin logic
            const response = await fetch("http://localhost:8000/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username_or_email: usernameOrEmail,
                    password: password,
                }),
            });

            if (!response.ok) {
                throw new Error("Signin failed");
            }

            const data = await response.json();
            // TODO: Store token and update auth state
            onClose();
            toast({
                title: "Success",
                description: "You have been signed in successfully",
                status: "success",
                duration: 3000,
                isClosable: true,
            });
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to sign in. Please check your credentials.",
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
                            value={usernameOrEmail}
                            onChange={(e) => setUsernameOrEmail(e.target.value)}
                            placeholder="Username or Email"
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
                        Sign In
                    </Button>
                </HStack>
            </form>
        </Box>
    );
} 