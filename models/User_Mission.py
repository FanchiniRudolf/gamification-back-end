from core.Model import *
from core.Utils import Utils
from models.User import User
from models.Mission import Mission


class User_Mission(Base, Model):
    __tablename__ = 'user_mission'

    student_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    mission_id = Column(BigInteger, ForeignKey(Mission.id), primary_key=True)
    grade = Column(Integer, default=None)
    comments = Column(String, default=None)

    studen = relationship(User)
    mission = relationship(Mission)
    

