from app import db
from sqlalchemy import Integer, String, DateTime, Boolean, Column
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(110))
    email = Column(String(110), unique=True)
    _passwd = Column("passwd", String(256)) 
    admin = Column(Boolean(), default=False)
    avatar = Column(String(110) , default='/static/img/avatar.png')
    phone = Column(String(20), default='0')
    created_at = Column(DateTime(), default=datetime.utcnow)

    @property
    def passwd(self):
        return self._passwd

    @passwd.setter
    def passwd(self, password):
        self._passwd = generate_password_hash(password)

    def IsOriginalPassword(self, password):
        return check_password_hash(self._passwd, password)

