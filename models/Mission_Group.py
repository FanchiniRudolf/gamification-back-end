from core.Model import *
from core.Utils import Utils
from models.Group import Group
from models.Mission import Mission


class Mission_Group(Base, Model):
    __tablename__ = 'mission_to_group'

    group_id = Column(BigInteger, ForeignKey(Group.id), primary_key=True)
    mission_id = Column(BigInteger, ForeignKey(Mission.id), primary_key=True)

    group = relationship(Group)
    mission = relationship(Mission)