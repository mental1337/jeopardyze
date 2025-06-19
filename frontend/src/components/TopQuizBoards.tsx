import { Box, Heading, Spinner, Text, useToast } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { TopQuizBoardModel, TopQuizBoardsResponse } from "../types/quiz_board_types";
import { useAuth } from "../contexts/AuthContext";
import api from "../lib/axios";
import { useNavigate } from "react-router-dom";

export default function TopQuizBoards() {
    const toast = useToast();
    const navigate = useNavigate();
    const { token, isGuest, user, guestId } = useAuth();
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<TopQuizBoardsResponse | null>(null);

    useEffect(() => {
        const fetchQuizBoards = async () => {
            try {
                const response = await api.get<TopQuizBoardsResponse>('/quiz-boards/top');
                setData(response.data);
                setError(null);
            } catch (err) {
                setError('Failed to load top quiz boards');
                toast({
                    title: "Error loading top quiz boards",
                    description: `Error: ${err}`,
                    status: "error",
                    duration: 5000,
                    isClosable: true,
                });
            } finally {
                setIsLoading(false);
            }
        };

        fetchQuizBoards();
    }, [toast]);

    const handleQuizBoardClick = async (boardId: number) => {
        try {
            let userId: number | null = null;
            let currentGuestId: number | null = null;

            // Use the guestId from AuthContext instead of parsing the token
            if (isGuest) {
                currentGuestId = guestId;
            } else if (user) {
                userId = user.id;
            }

            // Try to find an existing game session for this user/guest and quiz board
            let response = await api.get('/game-sessions/existing', {
                params: {
                    quiz_board_id: boardId,
                    user_id: userId,
                    guest_id: currentGuestId
                }
            });
            
            console.log("existing game session response", response);

            if (response.data?.game_session_id) {
                console.log("navigating to existing game session", response.data.game_session_id);
                navigate(`/play/${response.data.game_session_id}`);
                return;
            }

            // Create a new game session
            console.log("creating new game session");
            response = await api.post('/game-sessions/new-from-quiz-board/' + boardId);
            navigate(`/play/${response.data.game_session_id}`);
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to start game session",
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        }
    };

    return (
        <Box p={4} bg="gray.300" borderRadius="md" mt={4}>
            <Heading size="md" mb={4}>Top Games</Heading>
            <Box overflowX="auto">
                <Box as="table" width="100%" bg="white" borderRadius="md" borderWidth="1px">
                    <Box as="thead" bg="gray.50">
                        <Box as="tr">
                            <Box as="th" p={3} textAlign="center">Title</Box>
                            <Box as="th" p={3} textAlign="center">Creator</Box>
                            <Box as="th" p={3} textAlign="center">Times Played</Box>
                            <Box as="th" p={3} textAlign="center">Top Score</Box>
                            <Box as="th" p={3} textAlign="center">Scorer</Box>
                        </Box>
                    </Box>
                    <Box as="tbody">
                        {isLoading ? (
                            <Box as="tr">
                                <Box as="td" colSpan={5} p={4} textAlign="center">
                                    <Spinner />
                                </Box>
                            </Box>
                        ) : error ? (
                            <Box as="tr">
                                <Box as="td" colSpan={5} p={4} textAlign="center">
                                    <Text color="red.500">{error}</Text>
                                </Box>
                            </Box>
                        ) : data?.quiz_boards.length === 0 ? (
                            <Box as="tr">
                                <Box as="td" colSpan={5} p={4} textAlign="center">
                                    <Text>No quiz boards available</Text>
                                </Box>
                            </Box>
                        ) : (
                            data?.quiz_boards.map((board: TopQuizBoardModel) => (
                                <Box as="tr" key={board.id} borderTopWidth="1px">
                                    <Box 
                                        as="td" 
                                        p={3} 
                                        textAlign="center"
                                        cursor="pointer"
                                        _hover={{ bg: "gray.100" }}
                                        onClick={() => handleQuizBoardClick(board.id)}
                                    >
                                        {board.title}
                                    </Box>
                                    <Box as="td" p={3} textAlign="center">{board.creator}</Box>
                                    <Box as="td" p={3} textAlign="center">{board.total_sessions}</Box>
                                    <Box as="td" p={3} textAlign="center">{board.top_score}</Box>
                                    <Box as="td" p={3} textAlign="center">{board.top_scorer}</Box>
                                </Box>
                            ))
                        )}
                    </Box>
                </Box>
            </Box>
        </Box>
    );
}