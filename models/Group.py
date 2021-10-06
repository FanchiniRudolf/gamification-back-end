from core.Model import *
from core.Utils import Utils
from models.Course import Course
from models.Period import Period


# TODO Añadir parciales
class Group(Base, Model):
    __tablename__ = 'course_group'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey(Course.id), nullable=False)
    period_id = Column(BigInteger, ForeignKey(Period.id), nullable=False)
    name = Column(String, nullable=False)
    otp = Column(String(6), default=None)
    otp_time = Column(DateTime, default=None)
    created = Column(DateTime, default=Utils.time())
    updated = Column(DateTime, default=Utils.time(), onupdate=Utils.time())
    enable = Column(mysql.TINYINT(1), default=1)

    course = relationship(Course)
    period = relationship(Period)

    formatters = {
        "created": Utils.date_formatter, 
        "updated": Utils.date_formatter,
        "otp_time": Utils.date_formatter
    }