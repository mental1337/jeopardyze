import { Box, Button, FormControl, Input, HStack, useToast, Text } from "@chakra-ui/react";
import { useState } from "react";
import { VerifyEmailRequest, VerifyEmailResponse } from "../types/auth_types";
import api from "../lib/axios";

interface EmailVerificationBarProps {
    email: string;
    onVerificationSuccess: (response: VerifyEmailResponse) => void;
    onClose: () => void;
}

export default function EmailVerificationBar({ email, onVerificationSuccess, onClose }: EmailVerificationBarProps) {
    const [verificationCode, setVerificationCode] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const toast = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const request: VerifyEmailRequest = {
                email: email,
                code: verificationCode,
            };

            const { data } = await api.post<VerifyEmailResponse>('/auth/verify-email', request);

            onVerificationSuccess(data);
            onClose();
            toast({
                title: "Success",
                description: "Your email has been verified successfully!",
                status: "success",
                duration: 3000,
                isClosable: true,
            });
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail
                ? error.response.data.detail
                : "Failed to verify email. Please check your verification code.";
            
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

    const handleResendCode = async () => {
        setIsLoading(true);
        try {
            // Call the register endpoint again to resend verification code
            await api.post('/auth/register', {
                username: email.split('@')[0], // Use email prefix as username
                email: email,
                password: "temp_password" // This will be ignored since user already exists
            });
            
            toast({
                title: "Code Resent",
                description: "A new verification code has been sent to your email.",
                status: "info",
                duration: 3000,
                isClosable: true,
            });
        } catch (error: any) {
            toast({
                title: "Error",
                description: "Failed to resend verification code. Please try again.",
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box p={4} bg="yellow.100" borderRadius={10} mt={2} border="1px solid" borderColor="yellow.300">
            <form onSubmit={handleSubmit}>
                <HStack spacing={4} align="center">
                    <Text fontSize="sm" color="gray.700" minW="200px">
                        Verify your email ({email})
                    </Text>
                    
                    <FormControl isRequired maxW="150px">
                        <Input
                            type="text"
                            value={verificationCode}
                            onChange={(e) => setVerificationCode(e.target.value)}
                            placeholder="Enter 6-digit code"
                            size="sm"
                            bg="white"
                            maxLength={6}
                            pattern="[0-9]{6}"
                        />
                    </FormControl>

                    <Button
                        type="submit"
                        colorScheme="green"
                        isLoading={isLoading}
                        size="sm"
                        pl={4}
                        pr={4}
                    >
                        Verify
                    </Button>

                    <Button
                        type="button"
                        variant="outline"
                        colorScheme="blue"
                        isLoading={isLoading}
                        size="sm"
                        onClick={handleResendCode}
                        pl={4}
                        pr={4}
                    >
                        Resend
                    </Button>

                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={onClose}
                        pl={2}
                        pr={2}
                    >
                        ✕
                    </Button>
                </HStack>
            </form>
        </Box>
    );
} 