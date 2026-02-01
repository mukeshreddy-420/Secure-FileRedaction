
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import cursor, conn
import sqlite3

router = APIRouter()

class User(BaseModel):
    email: str
    password: str
    first_name: str = None
    last_name: str = None

@router.post("/signup")
def signup(user: User):
    try:
        cursor.execute("INSERT INTO users (email,password) VALUES (?,?)",(user.email,user.password))
        conn.commit()
        return {"message":"Signup success"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: User):
    try:
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?",(user.email,user.password))
        if cursor.fetchone():
            return {"email":user.email}
        return {"error":"Invalid credentials"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
