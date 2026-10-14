from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid, enum
from src.database import Base
class ConversationStatus(str, enum.Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    category = Column(String(100))
    total_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation")
class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    role = Column(String(20))
    content = Column(Text)
    cost = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")
