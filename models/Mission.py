from core.Model import *
from core.Utils import Utils
from models.MissionType import MissionType, User


class  Mission(Base, Model):
    __tablename__ = 'mission'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    teacher_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    type_id = Column(BigInteger, ForeignKey(MissionType.id), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default=None)
    xp = Column(Integer, nullable=False)
    
    type = relationship(MissionType)
