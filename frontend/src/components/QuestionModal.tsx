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
import { useState } from 'react';
import axios from 'axios';
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

    const handleSubmit = async () => {
        setIsSubmitting(true);
        try {
            const response = await axios.post<AnswerQuestionResponse>(
                `http://localhost:8000/api/game-sessions/${gameSessionId}/answer-question/${question.question_id}`,
                { answer: answer }
            );            
            // ^ Note that { answer: answer } is not the same as { "answer": answer }
            // Because In JavaScript/TypeScript object literals, the property name (left of the colon) is always taken literally, not as a variable.

            // Update the question in the parent component
            question.status = response.data.status as "unattempted" | "correct" | "incorrect";
            question.answer_text = response.data.correct_answer;
            question.points_earned = response.data.points_earned;
            question.user_answer = answer;

            onQuestionAnswered(question, response.data.updated_score);

            toast({
                title: response.data.status === 'correct' ? 'Correct!' : 'Incorrect :(',
                description: `Correct answer: ${response.data.correct_answer}`,
                duration: 5000,
                isClosable: true,
            });

            onClose();
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
            <ModalContent bg='gray.400'>
                <ModalHeader>Question for ${question.points}</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <VStack spacing={4} pb={4}>
                        <Text fontSize="lg">{question.question_text}</Text>
                        
                        {question.status === 'unattempted' ? (
                            // Show input and submit button for unanswered questions
                            <>
                                <Input
                                    placeholder="What / Who is ...?"
                                    value={answer}
                                    onChange={(e) => setAnswer(e.target.value)}
                                />
                                <Button
                                    colorScheme="blue"
                                    onClick={handleSubmit}
                                    isLoading={isSubmitting}
                                    isDisabled={!answer.trim()}
                                >
                                    Submit Answer
                                </Button>
                            </>
                        ) : (
                            // Show results for answered questions
                            <VStack spacing={2} align="stretch">
                                <Text>
                                    <strong>Your answer:</strong> {question.user_answer}
                                </Text>
                                <Text>
                                    <strong>Correct answer:</strong> {question.answer_text}
                                </Text>
                                <Text color={question.status === 'correct' ? 'green.500' : 'red.500'}>
                                    {question.status === 'correct' ? '✓ Correct' : '✗ Incorrect'}
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