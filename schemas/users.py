from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    email: EmailStr = Field(..., title="E-mail", description="Users e-mail.")
    password: str = Field(..., title="Password", description="Users password.")
