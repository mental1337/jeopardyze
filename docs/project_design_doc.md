# Project Jeopardyze - Design Document

## 1. System Overview
### 1.1 Purpose
Jeopardyze is a web application that generates Jeopardy-style quizzes using LLMs. It can create quizzes from uploaded documents, user-provided topics, or daily trending news.

### 1.2 System Architecture
```mermaid
graph LR
    subgraph "User Layer"
        User[<img src="https://raw.githubusercontent.com/mermaid-js/mermaid/master/docs/img/user.png" width="40" /> User <br/> End User]
    end
    
    subgraph "Presentation Layer"
        Frontend[<img src="https://raw.githubusercontent.com/mermaid-js/mermaid/master/docs/img/react.png" width="40" /> React Frontend <br/> User Interface]
    end
    
    subgraph "Application Layer"
        Backend[<img src="https://raw.githubusercontent.com/mermaid-js/mermaid/master/docs/img/python.png" width="40" /> FastAPI Backend <br/> Business Logic]
        Langchain[<img src="https://raw.githubusercontent.com/mermaid-js/mermaid/master/docs/img/ai.png" width="40" /> Langchain <br/> LLM Integration]
    end
    
    subgraph "Data Layer"
        Database[<img src="https://raw.githubusercontent.com/mermaid-js/mermaid/master/docs/img/database.png" width="40" /> PostgreSQL <br/> Data Storage]
    end

    User -- Interacts with --> Frontend
    Frontend -- REST API Calls --> Backend
    Backend -- Uses --> Langchain
    Backend -- Reads/Writes --> Database

    style Database fill:#fcc,stroke:#333,stroke-width:2px
```

## 2. Data Model

### 2.1 Database Schema
```mermaid
erDiagram
    QuizBoard ||--o{ Category : contains
    Category ||--o{ Question : contains
    QuizBoard ||--o{ GameSession : played_in
    User ||--o{ GameSession : plays
    GameSession ||--o{ QuestionAttempt : tracks

    QuizBoard {
        int id PK
        string title
        string source_type
        text source_content
        datetime created_at
    }

    Category {
        int id PK
        int quiz_board_id FK
        string name
    }

    Question {
        int id PK
        int category_id FK
        string question_text
        string answer
        int points
    }

    GameSession {
        int id PK
        int quiz_board_id FK
        int user_id FK
        int total_score
        datetime started_at
        datetime completed_at
        string status
    }

    QuestionAttempt {
        int id PK
        int game_session_id FK
        int question_id FK
        string user_answer
        boolean is_correct
        int points_earned
        datetime attempted_at
        string status
    }

    User {
        int id PK
        string username
        string email
        string password_hash
    }
```

## 3. API Design

### 3.1 Endpoints

#### Quiz Board Management
- `POST /api/quiz-boards/from-document`
  - Upload document or paste content
  - Returns generated quiz board

- `POST /api/quiz-boards/from-topic`
  - Accept topic/description
  - Returns generated quiz board

- `GET /api/quiz-boards`
  - List available quiz boards
  - Supports search and filtering

- `GET /api/quiz-boards/{id}`
  - Get specific quiz board details

#### Game Session
- `POST /api/game-sessions`
  - Start new game session
  - Returns session ID and initial state

- `GET /api/game-sessions/{id}`
  - Get game session details including:
    - Current score
    - Question states (unattempted/attempted/correct/wrong)
    - Attempted answers
    - Game status
    - Game progress
  - Response format:
    ```json
    {
        "gameSessionId": "string",
        "quizBoardId": "string",
        "totalScore": integer,
        "status": "in_progress",
        "questions": [
            {
                "questionId": "string",
                "category": "string",
                "points": integer,
                "status": "unattempted",
                "userAnswer": null,
                "isCorrect": null,
                "pointsEarned": 0
            }
        ],
        "progress": {
            "totalQuestions": integer,
            "attemptedQuestions": integer,
            "correctAnswers": integer,
            "wrongAnswers": integer
        }
    }
    ```

- `POST /api/game-sessions/{id}/questions/{questionId}/answer`
  - Submit answer for a question
  - Request body:
    ```json
    {
        "answer": "string"
    }
    ```
  - Response:
    ```json
    {
        "is_correct": boolean,
        "points_earned": integer,
        "correct_answer": "string",
        "updated_score": integer,
        "game_status": "string"
    }
    ```

#### User Management
- `POST /api/users/register`
- `POST /api/users/login`
- `GET /api/users/profile`

## 4. Frontend Design

### 4.1 Component Structure
```mermaid
graph TD
    App --> Navbar
    App --> HomePage
    App --> QuizBoardPage
    App --> GameSessionPage
    App --> AuthPage
    
    HomePage --> CreateFromTopic
    HomePage --> CreateFromDocument
    HomePage --> QuizBoardList
    
    CreateFromTopic --> FormInput
    CreateFromDocument --> FileUpload
    CreateFromDocument --> TextInput
    
    QuizBoardPage --> QuizGrid
    QuizGrid --> QuestionCard
    
    GameSessionPage --> ScoreDisplay
    GameSessionPage --> QuizGrid
    
    AuthPage --> LoginForm
    AuthPage --> RegisterForm
    LoginForm --> FormInput
    RegisterForm --> FormInput
```

### 4.2 Key Components
1. QuizBoardList
   - Displays available quiz boards
   - Shows top scores
   - Search functionality

2. QuizGrid
   - N x M grid display
   - Category headers
   - Question cards with point values

3. QuestionCard
   - Question display
   - Answer input
   - Point value display

4. ScoreDisplay
   - Current score
   - Game progress

## 5. User Flows and URL Structure

### 5.1 URL Patterns
```
/                   # Home page - Create quiz boards and list existing ones
/quiz-board/:id     # View a specific quiz board
/play/:id          # Play a specific quiz board
/profile           # User profile and game history
/login             # User login
/register          # User registration
```

### 5.2 User Flows

#### Quiz Board Creation Flow
1. Document-based Creation:
   ```
   / (Home page)
   ↓ (Upload document or paste content)
   POST /api/quiz-boards/from-document
   ↓ (Success)
   /quiz-board/:id
   ```

2. Topic-based Creation:
   ```
   / (Home page)
   ↓ (Enter topic)
   POST /api/quiz-boards/from-topic
   ↓ (Success)
   /quiz-board/:id
   ```

#### Game Play Flow
```
/quiz-board/:quizBoardId
↓ (Start game)
POST /api/game-sessions
↓ (Success - returns gameSessionId)
/play/:gameSessionId
↓ (Fetch all questions for the quiz board)
GET /api/quiz-boards/:quizBoardId/questions
↓ (Display game board with hidden questions)
/play/:gameSessionId
↓ (Select question card)
↓ (Display question modal with answer input)
↓ (Submit answer)
POST /api/game-sessions/:gameSessionId/questions/:questionId/answer
↓ (Backend validates answer using LLM and updates score)
↓ (Return response with validation result and updated score)
↓ (Update UI with answer result and new score)
↓ (Return to game board)
↓ (Repeat for each question)
↓ (Game complete - show completion modal)
/play/:gameSessionId
```

#### User Authentication Flow
```
/login or /register
↓ (Submit credentials)
POST /api/users/login or /api/users/register
↓ (Success)
/
```

### 5.3 Page Components and Features

#### Home Page (/)
- Create Game section with:
  - Topic input form
  - Document upload interface
  - Text input area for pasting content
  - Progress indicators for generation
  - Error handling for invalid inputs
- Existing Games section with:
  - Search bar for quiz boards
  - List of available quiz boards
  - Top scores display
  - Quick access to play games

#### Quiz Board Page (/quiz-board/:id)
- Quiz board grid display
- Category headers
- Question cards
- Start game button
- Share button
- View previous scores

#### Play Page (/play/:gameSessionId)
- Quiz board grid with:
  - Category headers
  - Question cards (initially showing point values)
  - Click handlers for each card
- Score display (updated after each answer)
- Question modal with:
  - Question display
  - Answer input box
  - Submit button
  - Feedback on answer correctness
- Game progress indicator
- Game completion modal (shown when all questions are answered) with:
  - Final score display
  - Share results button
  - Play again button
  - Return to home button
- Return to board button

#### Profile Page (/profile)
- User information
- Game history
- Statistics
- Achievements (future feature)

### 5.4 Navigation Structure
```mermaid
graph TD
    Home[Home] --> Profile[Profile]
    Home --> QuizBoard[Quiz Board]
    QuizBoard --> Play[Play]
    Play --> Profile
```

### 5.5 State Management
- Quiz board data
- Game session state:
  - Question states (unattempted/attempted/correct/wrong)
  - Attempted answers
  - Current score
  - Game progress
  - Game status (in_progress/completed)
- User authentication state
- UI state (modals, loading states)

#### Game Session State Example
```json
{
    "gameSessionId": "string",
    "quizBoardId": "string",
    "totalScore": integer,
    "status": "in_progress",
    "questions": [
        {
            "questionId": "string",
            "category": "string",
            "points": integer,
            "status": "unattempted",
            "userAnswer": null,
            "isCorrect": null,
            "pointsEarned": 0
        },
        {
            "questionId": "string",
            "category": "string",
            "points": integer,
            "status": "correct",
            "userAnswer": "string",
            "isCorrect": true,
            "pointsEarned": integer
        }
    ],
    "progress": {
        "totalQuestions": integer,
        "attemptedQuestions": integer,
        "correctAnswers": integer,
        "wrongAnswers": integer
    }
}
```

## 6. LLM Integration

### 6.1 Quiz Generation Process
1. Document Processing
   - Text extraction
   - Content analysis
   - Key topic identification

2. Category Generation
   - Topic clustering
   - Category naming
   - Difficulty distribution

3. Question Generation
   - Question-answer pair creation
   - Point value assignment
   - Answer validation

### 6.2 Prompt Engineering
- Document-based prompts
- Topic-based prompts
- News-based prompts

## 7. Security Considerations

### 7.1 Authentication
- JWT-based authentication
- Password hashing
- Session management

### 7.2 Data Protection
- Input validation
- SQL injection prevention
- XSS protection

## 8. Performance Considerations

### 8.1 Caching Strategy
- Quiz board caching
- User session caching
- API response caching

### 8.2 Database Optimization
- Indexing strategy
- Query optimization
- Connection pooling

## 9. Testing Strategy

### 9.1 Test Types
- Unit tests
- Integration tests
- End-to-end tests
- LLM response validation

### 9.2 Test Coverage
- API endpoints
- Database operations
- Frontend components
- LLM integration

## 10. Deployment Strategy

### 10.1 Infrastructure
- Containerization (Docker)
- CI/CD pipeline
- Monitoring and logging

### 10.2 Environment Setup
- Development
- Staging
- Production

## 11. Future Enhancements
1. Multiplayer support
2. Custom quiz board creation
3. Social features
4. Analytics dashboard
5. Mobile application

