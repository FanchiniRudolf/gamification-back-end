from core.Model import *
from core.Utils import Utils
from models.User import User

class Period(Base, Model):
    __tablename__ = 'period'

    id = Column(BigInteger, primary_key = True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created = Column(DateTime, default=Utils.time())
    updated = Column(DateTime, default=Utils.time(), onupdate=Utils.time())
    enable = Column(mysql.TINYINT(1), default=1)

    teacher = relationship(User)

    formatters = {"created": Utils.date_formatter, "updated": Utils.date_formatter}