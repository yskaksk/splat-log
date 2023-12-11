from datetime import datetime

from pydantic import BaseModel

from src.enum import Rule, Mode, Stage, Result


class BattleLog(BaseModel):
    id: int
    stage: Stage
    rule: Rule
    mode: Mode
    result: Result
    created_at: datetime


class BattleLogCreate(BaseModel):
    stage: Stage
    rule: Rule
    mode: Mode
    result: Result

    class Config:
        from_attributes = True


class BattleLogCreateResponse(BattleLogCreate):
    id: int

    class Config:
        from_attributes = True
