
interface TopQuizBoardModel {
    id: number;
    title: string;
    total_sessions: number;
    top_score: number;
    top_score_username: string;
    created_at: string;
}

interface TopQuizBoardsResponse {
    quiz_boards: TopQuizBoardModel[];
    total: number;
    limit: number;
    offset: number;
}

export type { TopQuizBoardModel, TopQuizBoardsResponse };