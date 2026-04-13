from pydantic import BaseModel, EmailStr, field_validator

# UserCreate is the payload the client sends to register a new user.
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# UserResponse is what the API returns — we never expose passwords or sensitive fields.
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

# UserSignup is used by the /signup-test endpoint to validate email + password format.
class UserSignup(BaseModel):
    username: str
    email: EmailStr  # EmailStr automatically validates that the value looks like an email
    password: str

    # field_validator("password") runs after the password field is parsed.
    # Raises ValueError (shown as a 422 response) if the rules aren't met.
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not v.isalnum():
            raise ValueError("Password must be alphanumeric (letters + numbers only).")
        return v