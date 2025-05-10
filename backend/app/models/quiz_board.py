from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import MyBaseModel, Base

class QuizBoard(MyBaseModel):
    __tablename__ = "quiz_boards"

    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    source_content = Column(Text, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    created_by_user = relationship("User", back_populates="quiz_boards")
    categories = relationship("Category", back_populates="quiz_board")

    