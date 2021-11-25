from core.Model import *
from core.Utils import Utils
from models.User_Group import User_Group
from models.Mission import Mission


class User_Mission(Base, Model):
    __tablename__ = 'user_mission'

    enrollment_id = Column(BigInteger, ForeignKey(User_Group.id), primary_key=True)
    mission_id = Column(BigInteger, ForeignKey(Mission.id), primary_key=True)
    grade = Column(Integer, default=None)
    xp = Column(Integer, default=None)
    coins=Column(Integer, default=0)
    comments = Column(String, default=None)

    enrollment = relationship(User_Group)
    mission = relationship(Mission)
    

