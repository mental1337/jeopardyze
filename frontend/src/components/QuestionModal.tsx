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
}

export default function QuestionModal({ isOpen, onClose, question, gameSessionId }: QuestionModalProps) {
    const [answer, setAnswer] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const toast = useToast();

    const handleSubmit = async () => {
        setIsSubmitting(true);
        try {
            console.log(`Submitting answer: ${answer} for question: ${question.question_id} in game session: ${gameSessionId}`);
            console.log(question);
            const response = await axios.post<AnswerQuestionResponse>(
                `http://localhost:8000/api/game-sessions/${gameSessionId}/answer-question/${question.question_id}`,
                { answer: answer }
            );            
            // ^ Note that { answer: answer } is not the same as { "answer": answer }
            // Because In JavaScript/TypeScript object literals, the property name (left of the colon) is always taken literally, not as a variable.

            toast({
                title: response.data.status === 'correct' ? 'Correct!' : 'Incorrect :(',
                description: `The correct answer was: ${response.data.correct_answer}`,
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
        <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>Question ({question.question_id}) for ${question.points}</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <VStack spacing={4} pb={4}>
                        <Text fontSize="lg">{question.question_text}</Text>
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
                    </VStack>
                </ModalBody>
            </ModalContent>
        </Modal>
    );
}