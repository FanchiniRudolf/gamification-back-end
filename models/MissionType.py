from core.Model import *
from core.Utils import Utils


class MissionType(Base, Model):
    __tablename__ = 'mission_type'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)