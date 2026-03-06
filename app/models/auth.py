from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator, Field

class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)


class Signup(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
    confirm_password: str = Field(..., min_length=6, max_length=255)

    @field_validator("confirm_password")
    def validate_confirm_password(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v
    

class authuser(BaseModel):
    id: int
    name: str
    email: EmailStr 