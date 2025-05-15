import { Box, Heading, Text, Button, useToast } from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function CreateFromText() {
    const [topic, setTopic] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate()
    const toast = useToast()

    const handleCreateQuiz = async () => {
        if (!topic.trim()) {
            toast({
                title: 'Error',
                description: 'Please enter a topic',
                status: 'error',
                duration: 3000,
                isClosable: true,
            })
            return
        }

        setIsLoading(true)
        try {
            const formData = new FormData()
            formData.append('topic', topic)

            const response = await axios.post('http://localhost:8000/api/quiz-boards/from-topic', formData)
            
            // Navigate to the game session page
            navigate(`/play/${response.data.game_session_id}`)
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to create quiz board',
                status: 'error',
                duration: 3000,
                isClosable: true,
            })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Box p={4} bg="gray.100" borderRadius="md">
            <Heading size="md" mb={2}>Create a Jeopardy quiz from any topic or description</Heading>
            <Box 
                as="textarea"
                p={2}
                borderWidth="1px"
                borderRadius="md"
                w="100%"
                h="100px"
                placeholder="Enter a topic or description..."
                resize="vertical"
                bg="white"
                value={topic}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setTopic(e.target.value)}
            />
            <Button 
                colorScheme="purple" 
                size="md" 
                onClick={handleCreateQuiz}
                isLoading={isLoading}
                loadingText="Creating Quiz..."
            >
                Create Quiz
            </Button>
        </Box>
    )
}