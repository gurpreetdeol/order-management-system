from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ecommerce import db
from ecommerce.orders.services import initiate_order, get_order_listing
from ecommerce.user.schema import User
from ecommerce.auth.jwt import get_current_user
from .schema import ShowOrder
from . import services
from . import schema

router = APIRouter(
    tags=["Orders"],
    prefix="/orders"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowOrder)
async def initiate_order_processing(database: Session = Depends(db.get_db),
                                    current_user: User = Depends(get_current_user)):
    result = await initiate_order(current_user, database)
    return result


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowOrder])
async def order_list(database: Session = Depends(db.get_db), current_user: User = Depends(get_current_user)):
    result = await get_order_listing(current_user, database)
    return result
