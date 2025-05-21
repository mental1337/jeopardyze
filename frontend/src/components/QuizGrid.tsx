import { Box, Flex, Grid, GridItem, Spacer, Text, useDisclosure } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import QuestionModal from './QuestionModal';

interface Category {
    id: number;
    name: string;
    questions: Question[];
}

interface Question {
    question_id: number;
    question_text: string;
    answer_text: string;
    points: number;

    user_answer: string | null;
    status: 'unattempted' | 'correct' | 'wrong';
    is_correct: boolean | null;
    points_earned: number;
}

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
                const response = await axios.get(`http://localhost:8000/api/game-sessions/${gameSessionId}`);
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
        if (question.status === 'unattempted') {
            setSelectedQuestion(question);
            onOpen();
        }
    };

    const getQuestionColor = (status: Question['status']) => {
        switch (status) {
            case 'correct':
                return 'green.500';
            case 'wrong':
                return 'red.500';
            default:
                return 'blue.600';
        }
    };

    return (
        <Box p={2} bg="gray.800" borderRadius="md">
            <Flex p={4} bg="gray.800" color="white" alignItems="center" borderRadius="0">
                <Text fontSize="lg" fontWeight="bold">
                    {quizTitle}
                </Text>
                <Spacer />
                <Text fontSize="md">
                    Score: ${score}
                </Text>
            </Flex>

            <Grid templateColumns={`repeat(${categories.length}, 1fr)`} gap={2} mt={2}>
                {categories.map((category) => (
                    <GridItem key={category.id}>
                        <Box bg="blue.800" color="white" p={4} borderRadius="0" h="20" mb={2}>
                            <Text fontWeight="bold" textAlign="center">{category.name}</Text>
                        </Box>
                        {category.questions.map((question) => (
                            <Box
                                key={question.question_id}
                                bg={getQuestionColor(question.status)}
                                color="gold"
                                p={4}
                                borderRadius="0"
                                mb={2}
                                cursor={question.status === 'unattempted' ? 'pointer' : 'default'}
                                onClick={() => handleQuestionClick(question)}
                                _hover={question.status === 'unattempted' ? { opacity: 0.8 } : {}}
                            >
                                <Text textAlign="center" fontWeight="bold" fontSize="xl">
                                    ${question.points}
                                </Text>
                            </Box>
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
                />
            )}
        </Box>
    );
}