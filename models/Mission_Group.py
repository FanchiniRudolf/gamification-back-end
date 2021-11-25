from core.Model import *
from core.Utils import Utils
from models.Group import Group
from models.Mission import Mission


class Mission_Group(Base, Model):
    __tablename__ = 'mission_to_group'

    group_id = Column(BigInteger, ForeignKey(Group.id), primary_key=True)
    mission_id = Column(BigInteger, ForeignKey(Mission.id), primary_key=True)
    average = Column(Float, default=0)
    start_date = Column(DateTime, nullable=False)
    delivery_date = Column(DateTime, nullable=False)

    group = relationship(Group)
    mission = relationship(Mission)

    formatters = {
        "delivery_date": Utils.date_formatter,
        "start_date": Utils.date_formatter
        }
