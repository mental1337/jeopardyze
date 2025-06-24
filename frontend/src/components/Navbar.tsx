import { Box, Text, Flex, HStack, Spacer, Link as ChakraLink, Menu, MenuButton, MenuList, MenuItem } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import SigninBar from "./SigninBar";
import SignupBar from "./SignupBar";
import EmailVerificationBar from "./EmailVerificationBar";
import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
    const [showSignin, setShowSignin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);
    const [showEmailVerification, setShowEmailVerification] = useState(false);
    const { player, isLoading, handleLoginSuccess, handleVerifyEmailSuccess, logout } = useAuth();
    
    // Listen for user token expiration events
    useEffect(() => {
        const handleUserTokenExpired = () => {
            console.log('User token expired event received, showing login modal');
            setShowSignin(true);
            setShowSignup(false);
            setShowEmailVerification(false);
        };

        window.addEventListener('userTokenExpired', handleUserTokenExpired);
        
        return () => {
            window.removeEventListener('userTokenExpired', handleUserTokenExpired);
        };
    }, []);
    

    // Show email verification bar when player is logged in but not verified
    useEffect(() => {
        if (player?.player_type === 'user' && player.email && player.is_verified === false) {
            setShowEmailVerification(true);
        }
        else {
            setShowEmailVerification(false);
        }
    }, [player]);

    
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

    const isLoggedIn = player?.player_type === 'user';
    const displayName = player?.display_name || 'Stranger';

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
                    <Text>Hi, {
                        isLoggedIn ? (
                            <UserMenu username={displayName} onSignOut={logout} />
                        ) : displayName
                    }!</Text>
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
                        <Text>to create.</Text>
                    </HStack>
                )}
            </Flex>
            
            {showSignin && <SigninBar onClose={() => setShowSignin(false)} onLoginSuccess={handleLoginSuccess}/>}
            {showSignup && <SignupBar onClose={() => setShowSignup(false)} onRegisterSuccess={handleLoginSuccess}/>}
            {showEmailVerification && (
                <EmailVerificationBar 
                    email={player?.email || ''}
                    onVerificationSuccess={handleVerifyEmailSuccess}
                    onClose={() => setShowEmailVerification(false)}
                />
            )}
        </Box>
    );
}

// Local component for the user menu dropdown
function UserMenu({ username, onSignOut }: { username: string; onSignOut: () => void }) {
    const handleSignOut = async () => {
        try {
            await onSignOut();
        } catch (error) {
            console.error('Error during sign out:', error);
        }
    };

    return (
        <Menu>
            <MenuButton as={ChakraLink} color="blue.500" _hover={{ textDecoration: "underline" }}>
                {username}
            </MenuButton>
            <MenuList minW="100px" p={0}>
                <MenuItem fontSize="sm" onClick={handleSignOut} px={3} py={2} justifyContent="center">Sign Out</MenuItem>
            </MenuList>
        </Menu>
    );
}