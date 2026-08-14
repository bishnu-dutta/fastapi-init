from app.users.model import User
from typing import Annotated
from fastapi import Depends
from .service import get_current_auth_user

CurrentUser = Annotated[User, Depends(get_current_auth_user)]
