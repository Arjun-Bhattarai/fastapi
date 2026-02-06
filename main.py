from fastapi import FastAPI

app = FastAPI()


@app.get("/{id}")
def root(id:int):
    return {"message":f"hello what are you doing {id} "}

@app.post("/todo")
def create_todo(item:dict):
    return {"message":"todo created ", "items":item}
