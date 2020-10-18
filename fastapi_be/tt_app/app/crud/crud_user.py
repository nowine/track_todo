from typing import Optional, List, Dict, Union, Any

from pydantic import EmailStr
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.core.security import encrypt_password, check_encrypted_password
from app.models import User
from app.schemas import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: EmailStr) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db:Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
                nickname=obj_in.nickname,
                fullname=obj_in.fullname,
                email=obj_in.email,
                hashed_password=encrypt_password(obj_in.password),
                is_active=obj_in.is_active,
                is_superuser=obj_in.is_superuser
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db:Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            update_data["hashed_password"] = encrypt_password(update_data['password'])
            del update_data["password"]
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db:Session, *, email: EmailStr, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not check_encrypted_password(password, user.hashed_password):
            return None
        return user
    
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_active(self, user:User) -> bool:
        return user.is_active


user = CRUDUser(User)
