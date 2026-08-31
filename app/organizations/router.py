from app.organizations.service import admin_create_post_for_user
from app.organizations.service import admin_delete_post_by_id_of_user
from app.organizations.service import admin_update_post_by_id_of_user
from app.posts.response import UpdatePrivatePostResponse
from app.organizations.service import admin_delete_user_by_id
from app.organizations.service import admin_update_user_by_id
from app.users.request import UpdateUserRequest
from app.users.service import get_user_by_id
from app.users.service import get_all_users
from app.users.model import User
from fastapi import status
from fastapi import APIRouter
from app.core.database import async_session_dep
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.response import PrivateUserResponse
from .request import AdminCreateUserRequest
from app.middleware.role_scope import admin
from .service import admin_add_user




router = APIRouter(prefix="/admin", tags=["organizations"], dependencies=[admin])

# ------ USER ------
@router.post("/create-user", 
            response_model=PrivateUserResponse,
            status_code=status.HTTP_201_CREATED, 
            summary="Create a new user by admin", 
            description="Create a new user in org by admin"
            )

async def admin_create_user(
    data: AdminCreateUserRequest,
    session: AsyncSession = async_session_dep,
    current_user: User = admin

):
    return await admin_add_user(data, session, current_user)
    
@router.get("/all", 
            response_model=list[PrivateUserResponse],
            status_code=status.HTTP_200_OK, 
            summary="Get all users", 
            description="Get all list of users of current organization from database(only public accessible data)"
            )

async def admin_get_all_users_api(
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await get_all_users(current_user, session)  

@router.get("/{id}", 
            response_model=PrivateUserResponse, 
            status_code=status.HTTP_200_OK, 
            summary="Get a user by id", 
            description="Get a user by id of current organization from database(only public accessible data)"
            )

async def admin_get_user_by_id_api(
    id: int,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await get_user_by_id(id, current_user, session)

@router.put("/{id}",
            response_model=PrivateUserResponse,
            status_code=status.HTTP_200_OK,
            summary="Update a user by id",
            description="Update a user by id of current organization from database(only public accessible data)"
)
async def admin_update_user_api(
    id: int,
    data: UpdateUserRequest,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_update_user_by_id(id, data, current_user, session)

@router.delete("/{id}", 
            response_model=PrivateUserResponse,
            status_code=status.HTTP_200_OK,
            summary="Delete a user by id",
            description="Delete a user by id from current organization from database(only public accessible data)"
)
async def admin_delete_user_api(
    id: int,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_delete_user_by_id(id, current_user, session)


# ------ POST ------


from app.posts.response import PrivatePostResponse
from app.posts.request import UpdatePostRequest
from app.posts.service import get_all_posts
from .service import admin_get_posts_by_id_of_user, admin_get_all_posts_of_user,admin_update_post_by_id_of_user, admin_delete_post_by_id_of_user
from app.posts.request import CreatePostRequest
from .service import admin_create_post_for_user


@router.get("/posts/all", 
            response_model=list[PrivatePostResponse],
            status_code=status.HTTP_200_OK, 
            summary="Get all posts", 
            description="Get all list of posts of current organization from database(only public accessible data)"
            )
async def admin_get_all_posts_api(
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await get_all_posts(current_user, session)

@router.get("/posts/user-id-{id}", 
            response_model=list[PrivatePostResponse],
            status_code=status.HTTP_200_OK, 
            summary="Get all posts of a user", 
            description="Get all list of posts of a user of current organization from database(only public accessible data)"
            )
async def admin_get_all_posts_of_user_api(
    id: int,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_get_all_posts_of_user(id, current_user, session)

@router.post("/posts/user-id-{id}",
            response_model=PrivatePostResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new post for a user",
            description="Create a new post for a user of current organization from database(only public accessible data)"
)
async def admin_create_post_api(
    id: int,
    data: CreatePostRequest,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_create_post_for_user(id, data, current_user, session)

@router.get("/posts/user-id-{owner_id}/post-id-{post_id}", 
            response_model=PrivatePostResponse,
            status_code=status.HTTP_200_OK, 
            summary="Get a post by id", 
            description="Get a post by id of a user of current organization from database(only public accessible data)"
            )
async def admin_get_post_by_id_api(
    owner_id:int,
    post_id: int,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_get_posts_by_id_of_user(owner_id,post_id,current_user, session)


@router.put("/posts/user-id-{owner_id}/post-id-{post_id}",
            response_model=UpdatePrivatePostResponse,
            status_code=status.HTTP_200_OK,
            summary="Update a post by id",
            description="Update a post by id of current organization from database(only public accessible data)"
)
async def admin_update_post_api(
    owner_id:int,
    post_id: int,
    data: UpdatePostRequest,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_update_post_by_id_of_user(owner_id, post_id, data, current_user, session)

@router.delete("/posts/user-id-{owner_id}/post-id-{post_id}", 
            response_model=PrivatePostResponse,
            status_code=status.HTTP_200_OK,
            summary="Delete a post by id",
            description="Delete a post by id from current organization from database(only public accessible data)"
)
async def admin_delete_post_api(
    owner_id:int,
    post_id: int,
    current_user: User = admin,
    session: AsyncSession = async_session_dep
):
    return await admin_delete_post_by_id_of_user(owner_id, post_id, current_user, session)

