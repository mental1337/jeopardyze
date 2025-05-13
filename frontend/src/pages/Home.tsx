import { useNavigate } from 'react-router-dom'
import { Container, VStack, Heading, Text, Button, Box, Spacer } from '@chakra-ui/react'
import Navbar from '../components/Navbar'
import CreateFromUpload from '../components/CreateFromUpload'
import CreateFromText from '../components/CreateFromText'
import ExistingQuizBoards from '../components/ExistingQuizBoards'

const Home = () => {
    const navigate = useNavigate()

    return (
        <>
            <Container maxW="container.md" centerContent>
                <VStack spacing={2} align="stretch" w="100%">

                    <Navbar />

                    {/* Second section - Topic description */}
                    <CreateFromText />

                    {/* Third section - Existing Quiz Boards */}
                    <ExistingQuizBoards />

                </VStack>
            </Container>
        </>
    )
}

export default Home;