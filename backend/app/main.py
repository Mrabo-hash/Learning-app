from fastapi import FastAPI, Depends, HTTPException, Request
from .ai_gemini import generate_learning_content
from .auth import create_access_token, oauth2_scheme
from .models import SessionLocal, User, Progress
from .gamification import award_badge
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/generate-quiz")
def generate_quiz(topic: str):
    prompt = f"Create a 5-question multiple-choice quiz for students about {topic}."
    quiz_text = generate_learning_content(prompt)
    return {"quiz": quiz_text}

@app.post("/api/progress")
def update_progress(user_id: int, module: str, score: int, db: Session = Depends(get_db)):
    progress = Progress(user_id=user_id, module=module, score=score, completed=score>=80)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    badge = None
    if score == 100:
        badge = award_badge(user_id, "Perfect Score")
    return {"progress": progress.id, "badge": badge}

@app.get("/api/recommendation")
def get_recommendation(user_id: int, db: Session = Depends(get_db)):
    # Demo: recommend next module based on progress
    return {"recommended_module": "Algebra II"}

@app.post("/api/token")
def login(form_data: Request, db: Session = Depends(get_db)):
    # Simplified: replace with actual user lookup and password verification
    data = await form_data.json()
    username, password = data["username"], data["password"]
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

# Add OAuth endpoints as needed (see FastAPI doc for OAuth2 integration)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
