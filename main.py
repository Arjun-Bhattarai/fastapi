from fastapi import FastAPI,Depends
from typing import Annotated
from test import  QueryParams

app = FastAPI()


@app.get("/")
def root(query: Annotated[QueryParams, Depends()]):
    return {"message":f"hello what are you doing", "params":query}

@app.post("/todo")
def create_todo(item:dict):
    return {"message":"todo created ", "items":item}
