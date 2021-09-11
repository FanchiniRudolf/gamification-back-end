from core.Model import *
from core.Utils import Utils
from models.Role import Role


class User(Base, Model):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(300), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(15), default=None)
    role_id = Column(BigInteger, ForeignKey(Role.id), default=Role.USER)
    otp = Column(String(6), default=None)
    otp_time = Column(DateTime, default=None)
    email_confirmation_code = Column(String(6), default=None)
    email_confirmation_code_time = Column(DateTime, default=None)
    confirmed_email = Column(mysql.TINYINT(1), default=0)
    created = Column(DateTime, default=Utils.time())
    updated = Column(DateTime, default=Utils.time(), onupdate=Utils.time())
    enable = Column(mysql.TINYINT(1), default=1)

    role = relationship(Role)

    formatters = {
        "created": Utils.date_formatter,
        "updated": Utils.date_formatter,
        "otp_time": Utils.date_formatter,
        "email_confirmation_code_time": Utils.date_formatter,
    }

    @staticmethod
    def check_if_user_exists(username, email):
        if username:
            check_username = User.get(User.username == username)
            if check_username:
                return True, "This username already exists"

        if email:
            check_email = User.get(User.email == email)
            if check_email:
                return True, "This email already has an account"

        return False, ""
