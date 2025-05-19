# filepath: c:\\ZTalJaZ\\AS\\Projects\\PhungQuangThang\\PQT_API\\routers\\PostRoute.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from pydantic import BaseModel
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from database import get_db, Base


# SQLAlchemy model for Post
class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    avatar_url = Column(Text)
    name = Column(String, nullable=False)
    created_at = Column(
        String, nullable=False, default=lambda: datetime.utcnow().isoformat()
    )
    description = Column(Text)
    location = Column(Text)
    image_url = Column(Text)


# Pydantic model for request body (creating a new post)
class PostCreate(BaseModel):
    avatar_url: str | None = None
    name: str
    description: str | None = None
    location: str | None = None
    image_url: str | None = None


# Pydantic model for response (reading a post)
class PostResponse(PostCreate):
    id: int
    created_at: str


router = APIRouter()


@router.get("/posts/", response_model=list[PostResponse])
async def read_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts


@router.post("/posts/", response_model=PostResponse, status_code=201)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    new_post_data = post.model_dump()
    # The database schema has created_at with a default CURRENT_TIMESTAMP,
    # and the SQLAlchemy model also has a default.
    # If we want to ensure created_at is set by the application:
    new_post_data["created_at"] = datetime.utcnow().isoformat()

    stmt = insert(Post).values(**new_post_data)
    result = await db.execute(stmt)
    await db.commit()
    created_post_id = result.inserted_primary_key[0]

    # Fetch the created post to return it
    created_post = await db.get(Post, created_post_id)
    if not created_post:
        raise HTTPException(status_code=404, detail="Post not found after creation")
    return created_post
