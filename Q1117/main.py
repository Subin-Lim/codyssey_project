# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 데이터베이스 테이블 생성 (필요시)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 의존성: 데이터베이스 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 질문 목록 조회
@app.get("/questions/")
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    return questions

# 새로운 질문 추가
@app.post("/questions/")
def create_question(subject: str, content: str, db: Session = Depends(get_db)):
    db_question = models.Question(subject=subject, content=content)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
