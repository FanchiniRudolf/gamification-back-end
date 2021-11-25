from core.Model import *
from core.Utils import Utils
from models.User import User
from models.Group import Group


class User_Group(Base, Model):
    __tablename__ = 'enrollment'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, ForeignKey(Group.id), nullable=False) 
    student_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    enable = Column(mysql.TINYINT(1), default=1)
    
    group = relationship(Group)
    student = relationship(User)


    def __repr__(self):
        return f'{self.student.username}'