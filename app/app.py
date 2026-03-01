from fastapi import FastAPI,Depends
from typing import Annotated
import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routing import todo
from app.config.app_config import get_app_config, AppConfig

app = FastAPI()

app.include_router(todo.router) # include the router from todo.py

@app.get("/")
def root():
    config=get_app_config()
    return {
        "message":"what are you doing",
        "app_name":config.app_name,
        "app_env":config.app_env,
        "database_url":config.database_url
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors={}
    for error in exc.errors():
        print(f"the error is: {error}")
        errors[error["loc"][-1]] = error["msg"]

    return JSONResponse(status_code=422, content={"message":"validation error", "errors":errors})


"""@app.post("/todo")
def create_todo(item:dict):
    return {"message":"todo created ", "items":item}"""

