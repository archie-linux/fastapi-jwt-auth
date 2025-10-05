from fastapi import FastAPI, Depends, HTTPException
from auth import authenticate_user, create_access_token, verify_role
from database import add_user
from datetime import timedelta
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.post("/register")
def register(user: User):
    if authenticate_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="User already exists")
    add_user(user.username, user.password)
    return {"message": "User registered successfully"}

@app.post("/token", response_model=TokenResponse)
def login(user: User):
    auth_user = authenticate_user(user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username, "role": auth_user["role"]},
                                       expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: dict = Depends(verify_role(["admin", "user"]))):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return {"message": "Protected data", "access_token": current_user}

@app.get("/admin")
def admin_route(user: dict = Depends(verify_role(["admin"]))):
    return {"message": "Welcome, Admin!"}

@app.get("/user")
def user_route(user: dict = Depends(verify_role(["admin", "user"]))):
    return {"message": "Hello, User!"}
