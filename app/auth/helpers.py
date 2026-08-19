from typing import Annotated

from fastapi import Depends

from app.users.model import User

from .service import get_current_auth_user

CurrentUser = Annotated[User, Depends(get_current_auth_user)]
