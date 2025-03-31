from fastapi import APIRouter, Depends
from models.user import User
from db import get_database, Session
from auth import get_user
from schemas.user import UserMe, UserMeUpdate
from typing import Optional
import errors

router = APIRouter(prefix="/users")

class UserService:
    @staticmethod
    def get_user_me(user: User) -> UserMe:
        return UserMe(
            id=user.id,
            name=user.user_info.name,
            email=user.email,
            username=user.username,
            surname=user.user_info.surname,
            patronymic=user.user_info.patronymic,  
            phone=user.user_info.phone,
            position=user.user_info.position,
            joined_at=user.user_info.joined_at
        )

    @staticmethod
    def update_user_info(
        db: Session,
        user: User,
        update_data: UserMeUpdate
    ) -> User:

        if not user:
            raise errors.unauthorized()

        user_info = user.user_info
        

        field_mapping = {
            'name': (user_info, 'name'),
            'email': (user, 'email'),
            'username': (user, 'username'),
            'surname': (user_info, 'surname'),
            'patronymic': (user_info, 'patronymic'),
            'phone': (user_info, 'phone'),
            'position': (user_info, 'position')
        }


        for field, (model, attr) in field_mapping.items():
            if getattr(update_data, field) is not None:
                setattr(model, attr, getattr(update_data, field))

        db.commit()
        return user

@router.get(
    '/me',
    response_model=UserMe,
    responses=errors.with_errors()
)
async def get_current_user(
    user: User = Depends(get_user),
    db: Session = Depends(get_database)
) -> UserMe:
    """Get current user profile"""
    return UserService.get_user_me(user)

@router.patch(
    '/me',
    response_model=UserMe,
    responses=errors.with_errors()
)
async def update_current_user(
    update_data: UserMeUpdate,
    user: User = Depends(get_user),
    db: Session = Depends(get_database)
) -> UserMe:
    updated_user = UserService.update_user_info(db, user, update_data)
    return UserService.get_user_me(updated_user)