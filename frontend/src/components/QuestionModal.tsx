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

interface Question {
    id: number;
    question_text: string;
    answer: string;
    points: number;
}

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
            const response = await axios.post(
                `http://localhost:8000/api/game-sessions/${gameSessionId}/questions/${question.id}/answer`,
                { answer }
            );
            
            toast({
                title: response.data.is_correct ? 'Correct!' : 'Incorrect',
                description: `The correct answer was: ${response.data.correct_answer}`,
                status: response.data.is_correct ? 'success' : 'error',
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
                <ModalHeader>Question for ${question.points}</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <VStack spacing={4} pb={4}>
                        <Text fontSize="lg">{question.question_text}</Text>
                        <Input
                            placeholder="What is ...?"
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