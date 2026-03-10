from fastapi import FastAPI
from src.books.routs import router 
from contextlib import asynccontextmanager

@asynccontextmanager  
def lifespan(app: FastAPI):
    print("Starting up...")
    yield # yield statement le startup code ra shutdown code bich ko execution lai separate garxa
    print("Shutting down...")

version = "v1"
app = FastAPI(
    lifespan=lifespan,
    title="Book API",
    description="A simple API for managing books",
    version=version,
)
app.include_router(router, prefix=f"/api/{version}/books")