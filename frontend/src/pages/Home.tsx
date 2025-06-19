import { useNavigate } from 'react-router-dom'
import { Container, VStack, Heading, Text, Button, Box, Spacer, Spinner, Center } from '@chakra-ui/react'
import Navbar from '../components/Navbar'
// import CreateFromUpload from '../components/CreateFromUpload'
import CreateFromText from '../components/CreateFromText'
import TopQuizBoards from '../components/TopQuizBoards'
import { useAuth } from '../contexts/AuthContext'

const Home = () => {
    const navigate = useNavigate()
    const { isLoading } = useAuth()

    // Show loading spinner while authentication is being initialized
    if (isLoading) {
        return (
            <Container maxW="container.md" centerContent>
                <Center h="50vh">
                    <VStack spacing={4}>
                        <Spinner size="xl" />
                        <Text>Initializing...</Text>
                    </VStack>
                </Center>
            </Container>
        )
    }

    return (
        <>
            <Container maxW="container.md" centerContent>
                <VStack spacing={2} align="stretch" w="100%">

                    <Navbar />

                    {/* Second section - Topic description */}
                    <CreateFromText />

                    {/* Third section - Existing Quiz Boards */}
                    <TopQuizBoards />

                </VStack>
            </Container>
        </>
    )
}

export default Home;