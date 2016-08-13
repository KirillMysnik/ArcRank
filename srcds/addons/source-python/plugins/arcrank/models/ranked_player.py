from sqlalchemy import Column, Integer, String, Text

from ..resource.config import config
from ..resource.sqlalchemy import Base


class RankedPlayer(Base):
    __tablename__ = (config['database']['prefix'] + "_" +
                     config['database']['server_id'] + "_" + "ranked_players")

    id = Column(Integer, primary_key=True)
    steamid = Column(String(32))
    last_used_name = Column(String(32))
    score = Column(Integer)
    position = Column(Integer)
    online_time = Column(Integer)
    detected_at = Column(Integer)
    last_seen_at = Column(Integer)
    data = Column(Text)
