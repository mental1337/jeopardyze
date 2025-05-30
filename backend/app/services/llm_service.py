from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain
import json
import os

from app.core.config import secrets
from app.core.logging import logger


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
        Create a Jeopardy-style quiz related to the following topic. You should create 3 categories that are related to the topic, and within each category, create 4 questions. As in the official Jeopardy game show, the questions must be in the form of a statement that provides a clue to the answer, and the answer should be a single word or phrase such that saying "What/Who is <answer>?" would be a valid question whose answer would be the clue statement.

        The category names should be short, interesting, possibly comprise of a pun or a play on words. Every question (clue statement) in the category should be related to the category name and to the given topic. Within a cateogy, the questions should have increasing difficulty.

        ```Topic:

        {topic}

        ```
        
        Return the results as a JSON object with the following structure:
        {{
            "title": "Quiz title based on the topic",
            "categories": [
                {{
                    "name": "Category 1 Name ",
                    "questions": [
                        {{
                            "question_text": "Question (clue statement)",
                            "correct_answer": "Answer text",
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
    logger.info(f"Test-Generating quiz board for topic: {topic}\n" + "="*50)

    quiz = llm_service.generate_quiz_board_from_topic("Marvel Cinematic Universe")
    
    # pretty print the quiz json:
    logger.info(json.dumps(quiz, indent=4))
    logger.info("="*50)
    


# Run this file as a script to test the LLM service
# python -m app.services.llm_services
if __name__ == "__main__":
    test_generate_quiz_board_from_topic()
