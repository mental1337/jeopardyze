# Project Jeopardyze

A website / webapp to create a jeopardy-style quiz using LLMs on any given topic or document.

## Requirements

1. User should be upload a document or copy-paste its contents into a text box, and the system should generate a Jeopardy-style quiz consisting of categories & questions based strictly on that document using an LLM (OpenAI API).

2. User should be able to type in a topic or a short description of something, and the system should create a Jeopardy-style quiz consisting of categories & questions about / surrounding that topic using an LLM.

3. The Jeopardy-style quiz consisting of categories & questions mentioned above shall be called a "Quiz Board", and it should:
    a. have N categories and M questions per category where N and M should ideally be 3 and 5 but may be fewer depending on amount of input content available.
    b. be displayed in a grid of N x M
    c. be playable by the user one question at a time
    d. have increasingly difficult questions in each category worth points of 100, 200, 300, 400, 500 each.

4. The system should generate a Quiz Board from trending news daily.

5. Every Quiz Board that was generated by any method should be selectable for play by any user later. When a user plays a Quiz Board, the played session shall be called a "Game Session".

6. Every Game Session shall have the score and user associated with it.

7. Available Quiz Boards should be displayed in a section on the front page showing the top score achieved for the Quiz Board. 

8. Quiz Boards should be findable by searching with a text input in a search box.

## Tech Stack to Use:

Backend: Python, FastAPI, PostgreSQL database, Langchain
Frontend: React


## More features to consider
- Teams score keeping?
- Replay a quizboard?
- Private or public quizboard - esp for from-document
