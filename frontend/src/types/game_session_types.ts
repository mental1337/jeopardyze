
// These frontend types should match the backend API schemas from backend/app/schemas

// This should match SessionQuestionPyd
interface Question {
    question_id: number;
    question_text: string;
    correct_answer: string | null;
    points: number;
    user_answer: string | null;
    status: 'unattempted' | 'correct' | 'incorrect';
    points_earned: number;
}

// This should match SessionCategoryPyd
interface Category {
    id: number;
    name: string;
    questions: Question[];
}

// This should match SessionQuizBoardPyd
interface QuizBoard {
    id: number;
    title: string;
    categories: Category[];
}

// This should match GameSessionResponse
interface GameSessionResponse {
    id: number;
    user_id: number;
    score: number;
    started_at: string;
    completed_at: string | null;
    status: string;
    session_quiz_board: QuizBoard;
}

// This should match AnswerQuestionResponse
interface AnswerQuestionResponse {
    question_id: number;
    status: string;
    correct_answer: string;
    points_earned: number;
    updated_score: number;
    game_status: string;
}

export type { Question, Category, QuizBoard, GameSessionResponse, AnswerQuestionResponse };