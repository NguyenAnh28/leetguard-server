from pydantic import BaseModel, EmailStr

# Schema for user registration input. Used when a new user signs up.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for user output. Used to return user information in API responses.
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Schema for signup response that includes email status
class SignupResponse(BaseModel):
    user: UserOut
    email_sent: bool
    message: str

    class Config:
        orm_mode = True

# Schema for email verification input. Used when a user submits their code.
class EmailVerificationInput(BaseModel):
    email: EmailStr
    code: str
