from core.Model import *
from core.Utils import Utils


class Role(Base, Model):
    # Roles
    TEACHER = 1
    STUDENT = 2

    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    created = Column(DateTime, default=Utils.time())
    updated = Column(DateTime, default=Utils.time(), onupdate=Utils.time())
    enable = Column(mysql.TINYINT(1), default=1, nullable=False)

    formatters = {"created": Utils.date_formatter, "updated": Utils.date_formatter}
