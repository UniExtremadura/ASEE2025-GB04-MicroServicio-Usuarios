from sqlalchemy.orm import Session
from app.models.usuario_model import User

def get_user_by_email(db: Session, email: str):
    """
    Retorna una instancia User o None.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    """
    Persiste una instancia User y la retorna con id/refresh.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user