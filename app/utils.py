from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import database
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

secret = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
expiration = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return context.hash(password)


def verify(user_password: str, hash_password: str):
    return context.verify(user_password, hash_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(expiration))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)

    return encoded_jwt


def verify_and_return_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(                    
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could  not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
        )

    try: 
        payload = jwt.decode(token, secret, algorithms=[algorithm])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    return id
    

def extract_crypto_details(data):
    crypto_list = []
    for item in data['data']:
        crypto = {
            "name": item["name"],
            "symbol": item["symbol"],
            "max_supply": item["max_supply"],
            "total_supply": item["total_supply"],
            "circulating_supply": item["circulating_supply"],
            "price": item["quote"]["USD"]["price"]
        }
        crypto_list.append(crypto)
    return crypto_list