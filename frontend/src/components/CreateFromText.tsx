import {  Box, Heading, Text, Button } from '@chakra-ui/react'

export default function CreateFromText() {
    return (
        <Box p={4} bg="gray.100" borderRadius="md">
            <Heading size="md" mb={2}>Or, create a Jeopardy quiz from any topic or description</Heading>
            <Box 
            as="textarea"
            p={2}
            borderWidth="1px"
            borderRadius="md"
            w="100%"
            h="100px"
            placeholder="Enter a topic or description..."
            resize="vertical"
            bg="white"
            />
            <Button colorScheme="purple" size="md">
            Create Quiz
            </Button>
        </Box>
    )
}