from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.battlelog as bs
import src.cruds.battlelog as bc
from src.db import get_db


router = APIRouter()


@router.get("/api/v1/battlelog", response_model=List[bs.BattleLog])
async def get_battlelog(db: AsyncSession = Depends(get_db)):
    return await bc.get_all_battlelog(db)


@router.post("/api/v1/battlelog", response_model=bs.BattleLogCreateResponse)
async def create_battlelog(
    body: bs.BattleLogCreate, db: AsyncSession = Depends(get_db)
):
    if body.mode == "レギュラーマッチ" and body.rule != "ナワバリバトル":
        raise HTTPException(status_code=400, detail="invalid rule")
    if body.rule == "ナワバリバトル" and body.mode != "レギュラーマッチ":
        raise HTTPException(status_code=400, detail="invalid mode")

    return await bc.create_battlelog(db, body)


@router.delete("/api/v1/battlelog/{id}", response_model=None)
async def delete_battlelog(id: int, db: AsyncSession = Depends(get_db)):
    log = await bc.get_battlelog(db, id)
    if log is None:
        raise HTTPException(status_code=404, detail="not found")
    return await bc.delete_battlelog(db, log)
