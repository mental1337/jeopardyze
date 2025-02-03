-- schema.sql
-- Database schema for Jeopardyze app

-- Users table for authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories for Jeopardy questions
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    points INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_points CHECK (points > 0)
);

-- Games table (represents a complete Jeopardy board)
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    created_by_user_id INTEGER REFERENCES users(id),
    prompt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mapping between games and their questions
CREATE TABLE game_questions (
    game_id INTEGER REFERENCES games(id),
    question_id INTEGER REFERENCES questions(id),
    PRIMARY KEY (game_id, question_id)
);

-- Game sessions (when a user plays a game)
CREATE TABLE game_sessions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    user_id INTEGER REFERENCES users(id),
    score INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'in_progress',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    CONSTRAINT valid_status CHECK (status IN ('in_progress', 'completed', 'abandoned'))
);

-- Track answers given in each session
CREATE TABLE session_answers (
    session_id INTEGER REFERENCES game_sessions(id),
    question_id INTEGER REFERENCES questions(id),
    user_answer TEXT,
    is_correct BOOLEAN,
    points_earned INTEGER,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id, question_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_questions_category ON questions(category_id);
CREATE INDEX idx_game_questions_game ON game_questions(game_id);
CREATE INDEX idx_game_sessions_user ON game_sessions(user_id);
CREATE INDEX idx_game_sessions_game ON game_sessions(game_id);
CREATE INDEX idx_session_answers_session ON session_answers(session_id);