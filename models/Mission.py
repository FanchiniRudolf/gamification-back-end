from core.Model import *
from core.Utils import Utils
from models.MissionType import MissionType


class Mission(Base, Model):
    __tablename__ = 'mission'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_id = Column(BigInteger, ForeignKey(MissionType.id), nullable=False)
    points = Column(Integer, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    xp = Column(Integer, nullable=False)
    coins = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)

    type = relationship(MissionType)

    formatters = {"delivery_date": Utils.date_formatter}
