from core.Model import *
from core.Utils import Utils
from models.User import User
from models.Group import Group


class User_Group(Base, Model):
    __tablename__ = 'enrollment'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, ForeignKey(Group.id), nullable=False) 
    student_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    hp = Column(Integer, default=0)
    