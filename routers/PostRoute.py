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
    name = Column(String, nullable=False)
    created_at = Column(
        String, nullable=False, default=lambda: datetime.utcnow().isoformat()
    )
    description = Column(Text, nullable=True)
    location = Column(Text, nullable=True)


# Pydantic model for request body (creating a new post)
class PostCreate(BaseModel):
    name: str
    description: str | None = None
    location: str | None = None


# Pydantic model for response (reading a post)
class PostResponse(BaseModel):
    id: int
    name: str
    created_at: str
    description: str | None = None
    location: str | None = None

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/posts/", response_model=list[PostResponse])
async def read_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts_db = result.scalars().all()
    response_posts = []
    for post_db_item in posts_db:
        response_posts.append(
            PostResponse(
                id=post_db_item.id,
                name=post_db_item.name,
                created_at=post_db_item.created_at,
                description=post_db_item.description,
                location=post_db_item.location,
            )
        )
    return response_posts


@router.post("/posts/", response_model=PostResponse, status_code=201)
async def create_post(
    post: PostCreate,  # Changed to accept PostCreate model as request body
    db: AsyncSession = Depends(get_db),
):
    new_post_db = Post(
        name=post.name,
        description=post.description,
        location=post.location,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(new_post_db)
    await db.commit()
    await db.refresh(new_post_db)

    return PostResponse(
        id=new_post_db.id,
        name=new_post_db.name,
        created_at=new_post_db.created_at,
        description=new_post_db.description,
        location=new_post_db.location,
    )
