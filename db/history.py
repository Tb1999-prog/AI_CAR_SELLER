from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import config

Base = declarative_base()

engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    history = Column(Text)


Base.metadata.create_all(bind=engine)
session = SessionLocal()


def get_history(session_id: str) -> str:
   
    conversation = session.query(Conversation).filter(Conversation.session_id == session_id).first()
    print("Fetched conversation:", conversation)
    session.close()
    return conversation.history if conversation else ""


def save_history(session_id: str, history: str):
    
    conversation = session.query(Conversation).filter(Conversation.session_id == session_id).first()

    if conversation:
        print("Existing conversation found. Updating it")
        conversation.history = history
    else:
        print("No existing conversation. Creating new one.")
        conversation = Conversation(session_id=session_id, history=history)
        session.add(conversation)

    session.commit()
    print("Saved conversation to DB.")
    session.close()


def print_all_conversations():
    session = SessionLocal()
    conversations = session.query(Conversation).all()
    for conv in conversations:
        print(f"Session ID: {conv.session_id}, History: {conv.history}")
    session.close()
