from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def create_user(db: Session, body: UserModel) -> User:
    user = User(**body.__dict__)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(user)
    return user


async def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def update_token(db: Session, user: User, token: str | None) -> None:
    user.update_token = token
    db.commit()
