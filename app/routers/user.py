from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from ..database import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.userResponse)
def create_user(user: schemas.createUser ,db: Session = Depends(get_session)):
    hashed_password =  utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    email_query = db.query(models.User).filter(models.User.email == user.email)
    if email_query.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email:{user.email} already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.userResponse)
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user