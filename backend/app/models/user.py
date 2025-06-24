from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class User(MyBaseModel):
    __tablename__ = "users"
    
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for guest users
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_code = Column(String(6), nullable=True)  # 6-digit verification code

    # Relationships
    player_profile = relationship("Player", back_populates="user", uselist=False)
    guests = relationship("Guest", back_populates="converted_to_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
