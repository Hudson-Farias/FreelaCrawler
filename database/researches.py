from sqlalchemy import Column, Integer, String
from database import Base

class ResearchesORM(Base):
    __tablename__ = 'researches'
    
    id = Column(Integer, primary_key=True, index=True)
    search = Column(String(255))
    channel_id = Column(Integer)