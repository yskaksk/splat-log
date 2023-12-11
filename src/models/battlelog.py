from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, Integer, String, DateTime


from src.db import Base


class BattleLog(Base):
    __tablename__ = "battlelog"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(255))
    rule = Column(String(255))
    stage = Column(String(255))
    result = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Tokyo")))
