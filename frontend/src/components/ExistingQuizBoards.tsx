import { Box, Heading } from "@chakra-ui/react";


export default function ExistingQuizBoards() {
    return (
        <Box p={4} bg="gray.100" borderRadius="md" mt={4}>
            <Heading size="md" mb={4}>Play existing Quiz Boards</Heading>
            <Box overflowX="auto">
                <Box as="table" width="100%" bg="white" borderRadius="md" borderWidth="1px">
                    <Box as="thead" bg="gray.50">
                        <Box as="tr">
                            <Box as="th" p={3} textAlign="center">Title</Box>
                            <Box as="th" p={3} textAlign="center">Top Score</Box>
                            <Box as="th" p={3} textAlign="center">User</Box>
                        </Box>
                    </Box>
                    <Box as="tbody">
                        {/* Sample data - replace with actual data */}
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">Science Quiz</Box>
                            <Box as="td" p={3} textAlign="center">2400</Box>
                            <Box as="td" p={3} textAlign="center">JohnDoe</Box>
                        </Box>
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">History Trivia</Box>
                            <Box as="td" p={3} textAlign="center">1800</Box>
                            <Box as="td" p={3} textAlign="center">JaneSmith</Box>
                        </Box>
                        <Box as="tr" borderTopWidth="1px">
                            <Box as="td" p={3} textAlign="center">Pop Culture</Box>
                            <Box as="td" p={3} textAlign="center">3200</Box>
                            <Box as="td" p={3} textAlign="center">QuizMaster</Box>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </Box>
    )
}