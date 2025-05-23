import { Box, Text } from '@chakra-ui/react';
import { Question } from '../types/game_session_types';

interface QuestionTileProps {
    question: Question;
    onClick: (question: Question) => void;
}

export default function QuestionTile({ question, onClick }: QuestionTileProps) {
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

    return (
        <Box
            bg="blue.600"
            color="gold"
            p={4}
            borderRadius="0"
            mb={2}
            cursor={question.status === 'unattempted' ? 'pointer' : 'default'}
            onClick={() => onClick(question)}
            _hover={question.status === 'unattempted' ? { opacity: 0.8 } : {}}
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