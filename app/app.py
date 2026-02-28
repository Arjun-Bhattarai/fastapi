from fastapi import FastAPI,Depends
from typing import Annotated
import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routing import todo

app = FastAPI()

app.include_router(todo.router) # include the router from todo.py

@app.get("/")
def root():
    return {"message":f"hello what are you doing"}

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

