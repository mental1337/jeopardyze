from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import MyBaseModel, Base

class QuizBoard(MyBaseModel):
    __tablename__ = "quiz_boards"

    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    source_content = Column(Text, nullable=False)
    created_by_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    # Relationships
    created_by_player = relationship("Player", back_populates="quiz_boards")
    categories = relationship("Category", back_populates="quiz_board")
    game_sessions = relationship("GameSession", back_populates="quiz_board")
    
    def __repr__(self):
        return f"<QuizBoard(id={self.id}, title={self.title}, #categories={len(self.categories)})>"
    