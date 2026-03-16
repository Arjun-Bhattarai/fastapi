from fastapi import FastAPI
from src.books.routs import router 
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager  
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield # yield statement le startup code ra shutdown code bich ko execution lai separate garxa
    print("Shutting down...")

version = "v1"
app = FastAPI(
    lifespan=lifespan,
    title="Book API",
    description="A simple API for managing books",
    version=version,
)
app.include_router(router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])