import { Box, Text, Flex, Heading, HStack, Spacer } from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <Flex p={4} bg="gray.300" alignItems="center" w="100%" borderRadius={10}>
            <Link to="/">
            <Text fontSize="xl" fontWeight="bold">
                Jeopardyze!
            </Text>
            </Link>
            <Spacer />
            
            <Spacer />
            <Box>
                <Link to="/profile">Profile</Link>
            </Box>

        </Flex>
    )
}