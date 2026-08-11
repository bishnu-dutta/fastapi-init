from .repository import (
    all_users,
    delete_user_by_id,
    find_user_by_email,
    find_user_by_id,
    save_user_to_database,
    update_user_by_id,
)
from .request import CreateUserRequest, UpdateUserRequest


def create_user(data: CreateUserRequest):
    existing_user = find_user_by_email(data.email)
    if existing_user:
        raise ValueError("User already exists")
    user = save_user_to_database(data)
    return user
    
    
def get_all_users():
    users = all_users()
    if users:
        return users
    else:
        raise ValueError("No users found")


def get_user_by_id(id: int):
    user = find_user_by_id(id)
    if user:
        return user
    else:
        raise ValueError("User not found")

def delete_user(id: int):
    user = delete_user_by_id(id)
    if user:
        return user
    else:
        raise ValueError("User not found")

def update_user(id:int, data:UpdateUserRequest):
    user = update_user_by_id(id,data)
    if user:
        return user
    else:
        raise ValueError("User not found")
