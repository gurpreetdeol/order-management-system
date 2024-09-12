from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ecommerce import db
# from ecommerce.auth.jwt import get_current_user
from . import schema
from . import services
from . import validator

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.User, database: Session = Depends(db.get_db)):
    user = await validator.verify_email_exist(request.email, database)
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system"
        )
    
    new_user = await services.new_user_registration(request, database)
    return new_user
