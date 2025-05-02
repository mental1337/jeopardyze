import {useNavigate} from 'react-router-dom'
import {Container, VStack, Heading, Text, Button, Box, Spacer} from '@chakra-ui/react'
import Navbar from '../components/Navbar'
const Home = () => {
    const navigate = useNavigate()

    return (
    <>
    <Container maxW="container.md" centerContent>
        <VStack spacing={2} align="stretch" w="100%">

        <Navbar />
        
        {/* First section - Document upload */}
        <Box p={4} bg="gray.100" borderRadius="md" mt={4}>
            <Heading size="md" mb={2}>Create a Jeopardy quiz from documents</Heading>
            <Box
            p={4}
            borderWidth="2px"
            borderRadius="md"
            borderStyle="dashed"
            borderColor="gray.300"
            bg="white"
            textAlign="center"
            mb={3}
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            h="120px"
            cursor="pointer"
            _hover={{ bg: "gray.50" }}
            onDrop={(e) => {
                e.preventDefault();
                const files = e.dataTransfer.files;
                // Handle files here
                console.log(files);
            }}
            onDragOver={(e) => {
                e.preventDefault();
            }}
            >
            <Text mb={2}>Drag and drop files here</Text>
            <Text fontSize="sm" color="gray.500">or</Text>
            </Box>
            <Button colorScheme="purple" size="md">
            Upload & Create Quiz
            </Button>
        </Box>
        
        {/* Second section - Topic description */}
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
        
        {/* Third section - Existing Quiz Boards */}
        <Box p={4} bg="gray.100" borderRadius="md" mt={4}>
            <Heading size="md" mb={4}>Play existing Quiz Boards</Heading>
            <Box overflowX="auto">
                <Box as="table" width="100%" bg="white" borderRadius="md" borderWidth="1px">
                    <Box as="thead" bg="gray.50">
                        <Box as="tr">
                            <Box as="th" p={3} textAlign="center">Title</Box>
                            <Box as="th" p={3} textAlign="center">Top Score</Box>
                            <Box as="th" p={3} textAlign="center">User</Box>
                        </Box>
                    </Box>
                    <Box as="tbody">
                        {/* Sample data - replace with actual data */}
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">Science Quiz</Box>
                            <Box as="td" p={3} textAlign="center">2400</Box>
                            <Box as="td" p={3} textAlign="center">JohnDoe</Box>
                        </Box>
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">History Trivia</Box>
                            <Box as="td" p={3} textAlign="center">1800</Box>
                            <Box as="td" p={3} textAlign="center">JaneSmith</Box>
                        </Box>
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">Pop Culture</Box>
                            <Box as="td" p={3} textAlign="center">3200</Box>
                            <Box as="td" p={3} textAlign="center">QuizMaster</Box>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </Box>


        
        </VStack>
    


    </Container>
    </>
    )
}

export default Home;