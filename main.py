from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.routes.todo import router   

app = FastAPI()

app.include_router(router) 

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "connected", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "details": str(e)}