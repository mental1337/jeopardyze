from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain
import json
import os

from app.core.config import secrets


class LLMService:
    def __init__(self):
        # self.llm = OpenAI(model="gpt-4o-mini", temperature=0.1, api_key=secrets.OPENAI_API_KEY)
        # ^ This is old api. It throws the following error:
        # openai.NotFoundError: Error code: 404 - {'error': {'code': None, 'message': 'Invalid URL (POST /v1/completions)', 'param': None, 'type': 'invalid_request_error'}}

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=secrets.OPENAI_API_KEY, streaming=False)
    
    def generate_quiz_board_from_topic(self, topic: str):
        """
        Generate a quiz board from a topic.
        """
        
        template_str = """
        You are a Jeopardy quiz creator. Create a Jeopardy-style quiz board based on the following topic:

        ```Topic:

        {topic}

        ```

        For this topic, create 5 relevant categories with 5 questions each. The questions should have increasing difficulty and point values 
        (200, 400, 600, 800, 1000).
        
        Return the results as a JSON object with the following structure:
        {{
            "title": "Quiz title based on the topic",
            "categories": [
                {{
                    "name": "Category 1 Name ",
                    "questions": [
                        {{
                            "question_text": "Question text",
                            "answer": "Answer text",
                            "points": 200
                        }},
                        ...
                    ]
                }},
                ...
            ]
        }}

        Note that JSON keys and values require to be withindouble-quotes. Double quotes within strings must be escaped with backslash, single quotes within strings shall not be escaped.
        """

        prompt = PromptTemplate(input_variables=["topic"],
                                template=template_str)

        chain = prompt | self.llm | JsonOutputParser()

        quiz = chain.invoke({"topic": topic})
        return quiz
        

def test_generate_quiz_board_from_topic():
    llm_service = LLMService()

    topic = "Marvel Cinematic Universe"
    print(f"Generating quiz board for topic: {topic}\n" + "="*50)

    quiz = llm_service.generate_quiz_board_from_topic("Marvel Cinematic Universe")
    # pretty print the quiz json:
    print(json.dumps(quiz, indent=4))
    print("="*50)
    


# Run this file as a script to test the LLM service
# python -m app.services.llm_services
if __name__ == "__main__":
    test_generate_quiz_board_from_topic()
