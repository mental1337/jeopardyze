import { Box, Text } from '@chakra-ui/react';
import { Question } from '../types/game_session_types';

interface QuestionBoxProps {
    question: Question;
    onClick: (question: Question) => void;
}

export default function QuestionBox({ question, onClick }: QuestionBoxProps) {
    const getQuestionStatusIcon = (status: Question['status']) => {
        switch (status) {
            case 'correct':
                return '✓';
            case 'incorrect':
                return '✗';
            default:
                return '';
        }
    };

    const getBoxStyles = (status: Question['status']) => {
        switch (status) {
            case 'unattempted':
                return {
                    bg: 'blue.600',
                    color: 'gold',
                    cursor: 'pointer',
                    _hover: { opacity: 0.7 }
                };
            case 'correct':
                return {
                    bg: 'gray.700',
                    color: 'gray.500',
                    cursor: 'default'
                };
            case 'incorrect':
                return {
                    bg: 'gray.700',
                    color: 'gray.500',
                    cursor: 'default'
                };
            default:
                return {
                    bg: 'blue.600',
                    cursor: 'pointer'
                };
        }
    };

    const styles = getBoxStyles(question.status);

    return (
        <Box
            p={4}
            borderRadius="0"
            mb={2}
            onClick={() => onClick(question)}
            {...styles}
        >
            <Text textAlign="center" fontWeight="bold" fontSize="xl">
                ${question.points}
                {question.status !== 'unattempted' && (
                    <Text as="span" ml={2} color={question.status === 'correct' ? 'green.500' : 'red.500'} fontSize="xl">
                        {getQuestionStatusIcon(question.status)}
                    </Text>
                )}
            </Text>
        </Box>
    );
} 