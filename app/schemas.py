from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserReponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class Crypto(BaseModel):
    id: int
    name: str
    symbol: str
    total_supply: int
    max_supply: int
    circulating_supply: int
    price: int
    
    model_config = ConfigDict(from_attributes=True)

