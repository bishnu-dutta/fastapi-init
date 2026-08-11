from fastapi import APIRouter

from .request import CreateUserRequest, UpdateUserRequest
from .response import UserResponse
from .service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserResponse)
def create_user_api(data:CreateUserRequest):
    return create_user(data)

@router.get("/all",response_model=list[UserResponse])
def get_all_users_api():
    return get_all_users()


@router.get("/{id}",response_model=UserResponse)
def get_user_by_id_api(id:int):
    return get_user_by_id(id)

@router.delete("/{id}",response_model=UserResponse)
def delete_user_api(id:int):
    return delete_user(id)

@router.put("/{id}",response_model=UserResponse)
def update_user_api(
    id:int,
    data:UpdateUserRequest
    ):
    return update_user(data)