import { Box, Text, Button, Heading } from '@chakra-ui/react'

export default function CreateFromUpload() {
    return (
        <Box p={4} bg="gray.100" borderRadius="md" mt={4}>
            <Heading size="md" mb={2}>Create a Jeopardy quiz from documents</Heading>
            <Box
                p={4}
                borderWidth="2px"
                borderRadius="md"
                borderStyle="dashed"
                borderColor="gray.300"
                bg="white"
                textAlign="center"
                mb={3}
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                h="120px"
                cursor="pointer"
                _hover={{ bg: "gray.50" }}
                onDrop={(e) => {
                    e.preventDefault();
                    const files = e.dataTransfer.files;
                    // Handle files here
                    console.log(files);
                }}
                onDragOver={(e) => {
                    e.preventDefault();
                }}
            >
                <Text mb={2}>Drag and drop files here</Text>
                <Text fontSize="sm" color="gray.500">or</Text>
                <Button
                    size="sm"
                    mt={2}
                    colorScheme="gray"
                    variant="outline"
                    onClick={() => {
                        const fileInput = document.getElementById('file-upload');
                        if (fileInput) {
                            fileInput.click();
                        }
                    }}
                >
                    Browse files
                </Button>
                <input
                    id="file-upload"
                    type="file"
                    multiple
                    style={{ display: 'none' }}
                    onChange={(e) => {
                        if (e.target.files) {
                            console.log(e.target.files);
                            // Handle files here
                        }
                    }}
                />
            </Box>
            <Button colorScheme="purple" size="md">
                Upload & Create Quiz
            </Button>
        </Box>

    )
}
