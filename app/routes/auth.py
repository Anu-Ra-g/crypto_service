from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, utils, models

router = APIRouter()

@router.get("/",status_code=status.HTTP_200_OK)
def welcome():
    return {"message": "Welcome to the backend service"}

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReponse)
def register(user: schemas.UserRequest, db: Session = Depends(database.get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token = utils.create_access_token({"user_id": user.id, "user_email": user.email})

    return {"access_token": access_token, "token_type": "Bearer"}