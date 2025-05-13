import { Box, Grid, GridItem, Text, useDisclosure } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import QuestionModal from './QuestionModal';

interface Category {
    id: number;
    name: string;
    questions: Question[];
}

interface Question {
    id: number;
    question_text: string;
    answer: string;
    points: number;
    status: 'unattempted' | 'attempted' | 'correct' | 'wrong';
}

interface QuizGridProps {
    gameSessionId: string;
}

export default function QuizGrid({ gameSessionId }: QuizGridProps) {
    const [categories, setCategories] = useState<Category[]>([]);
    const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null);
    const { isOpen, onOpen, onClose } = useDisclosure();

    useEffect(() => {
        const fetchGameSession = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/game-sessions/${gameSessionId}`);
                setCategories(response.data.categories);
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
            case 'attempted':
                return 'gray.500';
            default:
                return 'blue.500';
        }
    };

    return (
        <Box p={4} bg="gray.100" borderRadius="md">
            <Grid templateColumns={`repeat(${categories.length}, 1fr)`} gap={4}>
                {categories.map((category) => (
                    <GridItem key={category.id}>
                        <Box bg="blue.500" color="white" p={4} borderRadius="md" mb={4}>
                            <Text fontWeight="bold" textAlign="center">{category.name}</Text>
                        </Box>
                        {category.questions.map((question) => (
                            <Box
                                key={question.id}
                                bg={getQuestionColor(question.status)}
                                color="white"
                                p={4}
                                borderRadius="md"
                                mb={2}
                                cursor={question.status === 'unattempted' ? 'pointer' : 'default'}
                                onClick={() => handleQuestionClick(question)}
                                _hover={question.status === 'unattempted' ? { opacity: 0.8 } : {}}
                            >
                                <Text textAlign="center" fontWeight="bold">
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