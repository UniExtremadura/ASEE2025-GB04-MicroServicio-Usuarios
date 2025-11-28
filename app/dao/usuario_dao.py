from sqlalchemy.orm import Session
from app.models.usuario_model import User
from typing import Optional

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, email: str, **kwargs):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    """Elimina un usuario de la base de datos"""
    db.delete(db_user)
    db.commit()