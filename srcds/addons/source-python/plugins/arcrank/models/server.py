from sqlalchemy import Column, Integer, String

from ..resource.sqlalchemy import Base


class Server(Base):
    __tablename__ = "arcrank_schema_servers"

    id = Column(Integer, primary_key=True)
    server_id = Column(String(32))
    hostname = Column(String(128))
    total_positions = Column(Integer)
    last_sorted_at = Column(Integer)
