import { Box, Flex, Grid, GridItem, Spacer, Text, useDisclosure } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import api from '../lib/axios';
import QuestionModal from './QuestionModal';
import QuestionTile from './QuestionTile';
import { Question, Category, GameSessionResponse} from '../types/game_session_types';

interface QuizGridProps {
    gameSessionId: string;
}

export default function QuizGrid({ gameSessionId }: QuizGridProps) {
    const [score, setScore] = useState(0);
    const [quizTitle, setQuizTitle] = useState<string>('');
    const [categories, setCategories] = useState<Category[]>([]);
    const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null);
    const { isOpen, onOpen, onClose } = useDisclosure();

    useEffect(() => {
        const fetchGameSession = async () => {
            try {
                console.log(`Fetching game session ${gameSessionId}`)
                // const response = await axios.get(`http://localhost:8000/api/game-sessions/${gameSessionId}`);
                // const response = await axios.get<GameSessionResponse>(`http://localhost:8000/api/game-sessions/${gameSessionId}`);
                // const response = await api.get(`/game-sessions/${gameSessionId}`);
                const response = await api.get<GameSessionResponse>(`/game-sessions/${gameSessionId}`);
                // Now TypeScript knows the shape of response.data to be GameSessionResponse, and autocomplete helps

                console.log(`Received response: ${response.data}`)
                setQuizTitle(response.data.session_quiz_board.title);
                setCategories(response.data.session_quiz_board.categories);
                setScore(response.data.score);
                
            } catch (error) {
                console.error('Failed to fetch game session:', error);
            }
        };

        fetchGameSession();
    }, [gameSessionId]);

    const handleQuestionClick = (question: Question) => {
        setSelectedQuestion(question);
        onOpen();    
    };

    const updateQuestionAndScore = (updatedQuestion: Question, newScore: number) => {
        // Update the score
        setScore(newScore);

        // Update the question in the categories array
        setCategories(prevCategories => 
            prevCategories.map(category => ({
                ...category,
                questions: category.questions.map(q => 
                    q.question_id === updatedQuestion.question_id ? updatedQuestion : q
                )
            }))
        );
    };

    return (
        <Box p={2} bg="gray.800" borderRadius="md">
            <Flex p={4} bg="gray.800" color="white" alignItems="center" borderRadius="0">
                <Text fontSize="xl" fontWeight="bold" fontStyle="italic">
                    {quizTitle}
                </Text>
                <Spacer />
                <Text fontSize="xl" fontWeight="bold" color="gold">
                    Score: ${score}
                </Text>
            </Flex>

            <Grid templateColumns={`repeat(${categories.length}, 1fr)`} gap={2} mt={2}>
                {categories.map((category) => (
                    <GridItem key={category.id}>
                        <Box bg="blue.800" color="white" p={4} borderRadius="0" h="20" mb={2}>
                            <Text fontWeight="bold" textAlign="center" fontSize="lg">{category.name}</Text>
                        </Box>
                        {category.questions.map((question) => (
                            <QuestionTile
                                key={question.question_id}
                                question={question}
                                onClick={handleQuestionClick}
                            />
                        ))}
                    </GridItem>
                ))}
            </Grid>

            {selectedQuestion && (
                <QuestionModal
                    isOpen={isOpen}
                    onClose={onClose}
                    question={selectedQuestion}
                    gameSessionId={gameSessionId}
                    onQuestionAnswered={updateQuestionAndScore}
                />
            )}
        </Box>
    );
}