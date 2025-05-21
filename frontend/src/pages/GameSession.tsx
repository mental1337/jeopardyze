import { Box, Container, VStack } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import QuizGrid from '../components/QuizGrid';


const GameSession = () => {
    const { gameSessionId } = useParams();

    return (
        <Container maxW="container.xl" centerContent>
            <VStack spacing={4} align="stretch" w="100%">
                <Navbar />
                <QuizGrid gameSessionId={gameSessionId!} />
            </VStack>
        </Container>
    );
};

export default GameSession;