from pydantic import BaseModel, EmailStr, field_validator

class UserCreate :
    def __init__(self, username: str, email :str):
        self.username = username
        self.email = email

class UserResponse:
     def __init__(self, user_id : int , username : str , is_active : bool):
         self.user_id = user_id
         self.username = username
         self.is_active = is_active

class UserSignup(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not v.isalnum():
            raise ValueError("Password must be alphanumeric (letters + numbers only).")
        return v