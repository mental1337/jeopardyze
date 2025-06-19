import { Box, Text } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import api from '../lib/axios';

interface ScoreDisplayProps {
    gameSessionId: string;
}

export default function ScoreDisplay({ gameSessionId }: ScoreDisplayProps) {
    const [score, setScore] = useState(0);

    useEffect(() => {
        const fetchScore = async () => {
            try {
                const response = await api.get(`/game-sessions/${gameSessionId}`);
                setScore(response.data.total_score);
            } catch (error) {
                console.error('Failed to fetch score:', error);
            }
        };

        fetchScore();
    }, [gameSessionId]);

    return (
        <Box p={4} bg="blue.500" color="white" borderRadius="md">
            <Text fontSize="2xl" fontWeight="bold" textAlign="center">
                Score: ${score}
            </Text>
        </Box>
    );
}