import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    """Schema for creating a new post."""

    title: str = Field(
        ...,
        description="The title of the post",
        examples=["My First Post"],
    )
    content: str = Field(
        ...,
        description="The main text content of the post",
        examples=["This is the detailed content of the post."],
    )


class PostResponse(BaseModel):
    """Schema for a single post object response."""

    id: uuid.UUID = Field(
        ...,
        description="Unique identifier of the post",
    )
    user_id: uuid.UUID = Field(
        ...,
        description="Unique identifier of the post author",
    )
    title: str = Field(
        ...,
        description="The title of the post",
    )
    content: str = Field(
        ...,
        description="The main text content of the post",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the post was created",
    )

    class Config:
        from_attributes = True


class PostFeedItem(PostResponse):
    """Schema for a post item returned in the user feed, including ownership status."""

    is_owner: bool = Field(
        ...,
        description="True if the post belongs to the currently authenticated user, False otherwise",
    )


class FeedResponse(BaseModel):
    """Schema for the feed list response."""

    posts: list[PostFeedItem] = Field(
        ...,
        description="List of posts ordered by creation date descending",
    )


class MessageResponse(BaseModel):
    """simple status or confirmation response messages."""

    detail: str = Field(
        ...,
        description="Status message or detail description",
        examples=["Post deleted"],
    )


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schema for reading user details."""


class UserCreate(schemas.BaseUserCreate):
    """Schema for user registration request body."""


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user profile information."""
