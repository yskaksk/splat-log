from typing import List, Tuple
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


import src.models.battlelog as model
import src.schemas.battlelog as schema


async def create_battlelog(
    db: AsyncSession, body: schema.BattleLogCreate
) -> model.BattleLog:
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    log = body.dict()
    log["created_at"] = now
    battlelog = model.BattleLog(**log)
    db.add(battlelog)
    await db.commit()
    await db.refresh(battlelog)
    return battlelog


async def get_all_battlelog(db: AsyncSession) -> List[Tuple[int, str, str, str, str, datetime]]:
    result = await db.execute(select(
        model.BattleLog.id,
        model.BattleLog.mode,
        model.BattleLog.rule,
        model.BattleLog.stage,
        model.BattleLog.result,
        model.BattleLog.created_at
    ).order_by(model.BattleLog.created_at.desc()))
    return result.all()


async def get_battlelog(db: AsyncSession, id: int) -> model.BattleLog:
    return await db.get(model.BattleLog, id)


async def delete_battlelog(db: AsyncSession, log: model.BattleLog) -> None:
    await db.delete(log)
    await db.commit()
