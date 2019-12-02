from sqlalchemy import Column, Integer, String, Boolean, Float

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.gift import Gift
from app.models.wish import Wish
from yushu_book import YuShuBook


class User(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer(), default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    _password = Column('password', String(128), nullable=False)

    # 用户传进来的密码是明文的   服务器是需要对明文的密码进行加密的 不能够在数据库中明文保存密码

    # 属性读取
    @property
    def password(self):
        return self._password

    # 属性写入
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # check_password_hash 完成了先加密后比较的操作  返回值为bool值
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # def get_id(self):
    #     pass

    # 检测isbn
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 对一本书，一个用户不能同时是赠送者和索要者
        # 也就是必须这本要赠送的图书 即不在清单中  也不再心愿清单中

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False


# 这个函数的内部实现 把id号转化成了对象模型
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
