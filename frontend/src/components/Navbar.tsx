import { Box, Text, Flex, Heading, HStack, Spacer, Link as ChakraLink } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { useState } from "react";
import SigninBar from "./SigninBar";
import SignupBar from "./SignupBar";

export default function Navbar() {
    const [showSignin, setShowSignin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);
    const isLoggedIn = false; // TODO: Replace with actual auth state

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
                {isLoggedIn ? (
                    <Box>
                        <Link to="/profile">Profile</Link>
                    </Box>
                ) : (
                    <HStack spacing={2}>
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
            
            {showSignin && <SigninBar onClose={() => setShowSignin(false)}/>}
            {showSignup && <SignupBar onClose={() => setShowSignup(false)}/>}
        </Box>
    );
}