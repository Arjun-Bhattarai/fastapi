from pydantic import BaseModel,Field

class UserCreate(BaseModel):
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    password: str = Field(min_length=5,max_length=100)