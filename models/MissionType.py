from core.Model import *
from core.Utils import Utils
from models.User import User


class MissionType(Base, Model):
    __tablename__ = 'mission_type'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    teacher_id = Column(BigInteger, ForeignKey(User.id), default=None)

    teacher = relationship(User)