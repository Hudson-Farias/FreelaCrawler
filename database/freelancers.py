from sqlalchemy import Column, Integer, String
from database import Base

class FreelancersORM(Base):
    __tablename__ = 'freelancers'
    
    id = Column(Integer, primary_key=True, index=True)
    search = Column(String(255))
    channel_id = Column(Integer)