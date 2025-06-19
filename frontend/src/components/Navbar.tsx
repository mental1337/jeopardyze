import { Box, Text, Flex, Heading, HStack, Spacer, Link as ChakraLink } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { useState } from "react";
import SigninBar from "./SigninBar";
import SignupBar from "./SignupBar";
import { useAuth } from "../contexts/AuthContext";
import { RegisterResponse } from "../types/auth_types";

export default function Navbar() {
    const [showSignin, setShowSignin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);
    const { token, isGuest, user, isLoading, guestId, handleLoginSuccess, handleVerifyEmailSuccess } = useAuth();
    
    // Handle successful registration (just close the form)
    const handleRegisterSuccess = (response: RegisterResponse) => {
        setShowSignup(false);
        // User will need to verify email before they can log in
    };
    
    // Don't show auth state while loading
    if (isLoading) {
        return (
            <Box bg="gray.300" borderRadius={10}>
                <Flex p={4} alignItems="center" w="100%">
                    <Link to="/">
                        <Text fontSize="xl" fontWeight="bold">
                            Jeopardyze!
                        </Text>
                    </Link>
                    <Spacer />
                </Flex>
            </Box>
        );
    }

    const isLoggedIn = !isGuest && user !== null;
    
    // Determine the name to display
    const displayName = isLoggedIn ? user?.username : `Guest-${guestId}`;

    return (
        <Box bg="gray.300" borderRadius={10}>
            <Flex p={4} alignItems="center" w="100%">
                <Link to="/">
                    <Text fontSize="xl" fontWeight="bold">
                        Jeopardyze!
                    </Text>
                </Link>
                <Spacer />
                
                <Spacer />
                <Box>
                    <Text>Hi {displayName}!</Text>
                    {isLoggedIn && <Link to="/profile">Profile</Link>}
                </Box>
                {!isLoggedIn && (
                    <HStack spacing={2} ml={4}>
                        <ChakraLink 
                            onClick={() => {
                                setShowSignin(true);
                                setShowSignup(false);
                            }}
                            color="blue.500"
                            _hover={{ textDecoration: "underline" }}
                        >
                            Signin
                        </ChakraLink>
                        <Text>or</Text>
                        <ChakraLink 
                            onClick={() => {
                                setShowSignup(true);
                                setShowSignin(false);
                            }}
                            color="blue.500"
                            _hover={{ textDecoration: "underline" }}
                        >
                            Signup
                        </ChakraLink>
                        <Text>to save progress</Text>
                    </HStack>
                )}
            </Flex>
            
            {showSignin && <SigninBar onClose={() => setShowSignin(false)} onLoginSuccess={handleLoginSuccess}/>}
            {showSignup && <SignupBar onClose={() => setShowSignup(false)} guestId={guestId?.toString()} onRegisterSuccess={handleRegisterSuccess}/>}
        </Box>
    );
}