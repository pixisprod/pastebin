from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=50, examples=['user@corp.com'])
    password: str = Field(min_length=1, max_length=50, examples=['qwerty123'])