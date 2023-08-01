from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import utils, database, models, schemas
from typing import List
from . import callapi

router = APIRouter()


@router.get("/cryptos", response_model=schemas.Crypto, status_code=status.HTTP_200_OK)
def list_all_cryptodetails(db: Session = Depends(database.get_db), user_id: int = Depends(utils.verify_and_return_user)):

    crypto_details = db.query(models.Crypto).all()

    return crypto_details






