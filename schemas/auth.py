from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    jwt_token: str
