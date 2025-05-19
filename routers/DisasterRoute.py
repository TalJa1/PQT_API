from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, selectinload
from pydantic import BaseModel
import sys
import os
from typing import List

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import get_db, Base


# SQLAlchemy model for ThienTai (Disasters)
class ThienTai(Base):
    __tablename__ = "ThienTai"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    actions = relationship("Action", back_populates="thien_tai", lazy="selectin")


# SQLAlchemy model for Actions
class Action(Base):
    __tablename__ = "Actions"

    action_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thien_tai_id = Column(
        Integer, ForeignKey("ThienTai.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    thien_tai = relationship("ThienTai", back_populates="actions")


# Pydantic model for Action response
class ActionResponse(BaseModel):
    action_id: int
    thien_tai_id: int
    title: str
    description: str

    class Config:
        from_attributes = True


# Pydantic model for ThienTai response
class ThienTaiResponse(BaseModel):
    id: int
    name: str
    actions: List[ActionResponse] = []

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/thientai/", response_model=List[ThienTaiResponse])
async def read_thien_tai_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ThienTai).options(selectinload(ThienTai.actions)))
    thien_tai_list = result.scalars().unique().all()
    return thien_tai_list


@router.get("/thientai/{thien_tai_id}", response_model=ThienTaiResponse)
async def read_thien_tai_by_id(thien_tai_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ThienTai)
        .where(ThienTai.id == thien_tai_id)
        .options(selectinload(ThienTai.actions))
    )
    thien_tai = result.scalars().unique().first()
    if thien_tai is None:
        raise HTTPException(status_code=404, detail="ThienTai not found")
    return thien_tai
