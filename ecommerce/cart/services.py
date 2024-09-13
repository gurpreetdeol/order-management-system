from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ecommerce import db
from ecommerce.products.models import Product
from ecommerce.user.models import User
from .models import Cart, CartItems
from . import schema


async def add_items(cart_id, product_id, database: Session = Depends(db.get_db)):
    cart_items = CartItems(cart_id=cart_id, product_id=product_id)
    database.add(cart_items)
    database.commit()
    database.refresh(cart_items)


async def add_to_cart(product_id: int, database: Session = Depends(db.get_db)):
    product_info = database.query(Product).get(product_id)
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")

    if not product_info.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Out of Stock!")

    user_info = database.query(User).filter(User.email == "deol.gs@gmail.com").first()

    cart_info = database.query(Cart).filter(Cart.user_id == user_info.id).first()
    if not cart_info:
        new_cart = Cart(user_id=user_info.id)
        database.add(new_cart)
        database.commit()
        database.refresh(new_cart)
        await add_items(new_cart.id, product_info.id, database)
    else:
        await add_items(cart_info.id, product_info.id, database)
    return {"status": "Item added to cart!"}


async def get_all_items(database) -> schema.ShowCart:
    user_info = database.query(User).filter(User.email == "deol.gs@gmail.com").first()
    cart = database.query(Cart).filter(Cart.user_id == user_info.id).first()
    return cart


async def remove_cart_item(cart_item_id: int, database):
    user_info = database.query(User).filter(User.email == "deol.gs@gmail.com").first()
    cart_info = database.query(Cart).filter(User.id == user_info.id).first()
    database.query(CartItems).filter(and_(CartItems.id == cart_item_id, CartItems.cart_id == cart_info.id)).delete()
    database.commit()
    return {"status": "Item removed from cart!"}
