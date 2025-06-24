import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalCloseButton,
    Button,
    VStack,
    Text,
    Input,
    useToast,
} from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import api from '../lib/axios';
import { Question, AnswerQuestionResponse } from '../types/game_session_types';

interface QuestionModalProps {
    isOpen: boolean;
    onClose: () => void;
    question: Question;
    gameSessionId: string;
    onQuestionAnswered: (updatedQuestion: Question, newScore: number) => void;
}

export default function QuestionModal({ isOpen, onClose, question, gameSessionId, onQuestionAnswered }: QuestionModalProps) {
    const [answer, setAnswer] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const toast = useToast();

    // Reset answer when modal is opened with a new question
    useEffect(() => {
        if (isOpen) {
            setAnswer('');
        }
    }, [isOpen, question.question_id]);

    const handleSubmit = async (e?: React.FormEvent) => {
        // Prevent default form submission if event exists
        e?.preventDefault();
        
        setIsSubmitting(true);
        try {
            const response = await api.post<AnswerQuestionResponse>(
                `/game-sessions/${gameSessionId}/answer-question/${question.question_id}`,
                { answer: answer }
            );            
            // ^ Note that { answer: answer } is not the same as { "answer": answer }
            // Because In JavaScript/TypeScript object literals, the property name (left of the colon) is always taken literally, not as a variable.

            // Update the question in the parent component
            question.status = response.data.status as "unattempted" | "correct" | "incorrect";
            question.correct_answer = response.data.correct_answer;
            question.points_earned = response.data.points_earned;
            question.user_answer = answer;

            onQuestionAnswered(question, response.data.updated_score);

            // toast({
            //     title: response.data.status === 'correct' ? 'Correct!' : 'Incorrect :(',
            //     description: `Correct answer: ${response.data.correct_answer}`,
            //     duration: 5000,
            //     isClosable: true,
            // });

        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to submit answer',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} isCentered scrollBehavior='inside' size='xl'>
            <ModalOverlay />
            <ModalContent bg='purple.800' color='white'>
                <ModalHeader>Question for ${question.points}</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <VStack spacing={4} pb={4}>
                        <Text fontSize="lg">{question.question_text}</Text>
                        
                        {question.status === 'unattempted' ? (
                            // Show input and submit button for unanswered questions
                            <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                                <VStack spacing={4} width="100%">
                                    <Input
                                        placeholder="What / Who is ...?"
                                        value={answer}
                                        onChange={(e) => setAnswer(e.target.value)}
                                    />
                                    <Button
                                        type="submit"
                                        colorScheme="blue"
                                        isLoading={isSubmitting}
                                        isDisabled={!answer.trim()}
                                        width="100%"
                                    >
                                        Submit Answer
                                    </Button>
                                </VStack>
                            </form>
                        ) : (
                            // Show results for answered questions
                            <VStack spacing={2} align="stretch">
                                <Text color={question.status === 'correct' ? 'green.500' : 'red.500'} fontWeight="bold">
                                    {question.status === 'correct' ? '✓ Correct' : '✗ Incorrect'}
                                </Text>
                                <Text>
                                    <strong>Correct answer:</strong> {question.correct_answer}
                                </Text>
                                <Text>
                                    <strong>Your answer:</strong> {question.user_answer}
                                </Text>
                                <Text>
                                    <strong>Points earned:</strong> {question.points_earned}
                                </Text>
                            </VStack>
                        )}
                    </VStack>
                </ModalBody>
            </ModalContent>
        </Modal>
    );
}