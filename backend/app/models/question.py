from sqlalchemy import Column, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class Question(MyBaseModel):
    __tablename__ = "questions"
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    points = Column(Integer, nullable=False)

    # Relationships
    category = relationship("Category", back_populates="questions")
    
    