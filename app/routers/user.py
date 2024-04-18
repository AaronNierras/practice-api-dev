from fastapi import status, Response, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from .. import models, schemas, database, utils


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/orm/{id}', response_model=schemas.UserResponse)
async def get_user_orm(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.DBUser).filter(models.DBUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user


@router.post('/orm', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
async def create_user_orm(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_pass = utils.hass_pass(user.password)
    user.password = new_pass
    new_user = models.DBUser(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user