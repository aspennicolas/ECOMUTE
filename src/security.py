from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import get_db

SECRET_KEY = "your-secret-key"  # Replace with a strong random key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# These functions are used for hashing passwords and verifying them. When a user registers, we will hash their password using get_password_hash() before storing it in the database. When they log in, we will use verify_password() to check if the provided password matches the hashed password in the database.
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(plain: str) -> str:
    return pwd_context.hash(plain)

# This function creates a JWT access token. The data parameter is a dictionary that should contain at least the "sub" claim (the username) and the "role" claim (the user's role). The token will also include an expiration time set to 30 minutes from the time of creation. The token is signed using the SECRET_KEY and the specified ALGORITHM.
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# This is the OAuth2 scheme that FastAPI will use to extract the token from the Authorization header of incoming requests. The tokenUrl is the URL where clients can obtain a token (e.g. by providing username and password). In this case, we will implement that endpoint at /auth/token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# This function will be used as a dependency in routes that require authentication. It decodes the JWT token, verifies it, and retrieves the corresponding user from the database.
async def get_current_user(
    token: str = Depends(oauth2_scheme), # FastAPI will use the oauth2_scheme to extract the token from the request and pass it in here.
    db: AsyncSession = Depends(get_db), # FastAPI will call get_db() to get an async database session and pass it in here.
):
    from src.data.models import User  # local import to avoid circular dependency
    # We define a reusable HTTPException for invalid credentials to avoid repeating the same code in multiple places.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # The "sub" claim in the JWT is typically used to store the username or user ID.
        role: str = payload.get("role") # We also include the user's role in the token so we can check it for authorization.
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username)) # We query the database for a user with the given username. scalar_one_or_none() will return the User object if found, or None if no user with that username exists.
    user = result.scalar_one_or_none() 
    if user is None:
        raise credentials_exception
    return user # If we found the user, we return it. This user object will be available in any route that uses get_current_user as a dependency!!!


def require_role(role: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to {role} role",
            )
        return current_user
    return role_checker
