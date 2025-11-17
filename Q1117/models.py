# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLAlchemy의 기본 클래스
Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    # 필드 정의
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    content = Column(Text)
    create_date = Column(DateTime, default=datetime.utcnow)
