from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, SmallInteger, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from flask_login import UserMixin
from app.models.wish import Wish
from yushu_book import YuShuBook
from collections import namedtuple


# namedtuple  快速定义对象的工具


# 模型只负责提供原始数据
# 所有处理viewmodel 应该在视图函数中进行（专门写入 viewmodel）
# 可以视为原则

class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 这里gift对应的book  就使用isbn编号    （因为这个项目的book是在接口中获取而不是数据库中，所以无法用外键  换种思路）
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)  # 是否被增送

    # 当前用户所有的礼物 倒序排列
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        根据传入的一组isbn， 到wish表中计算出某个礼物的Wish心愿数量
        db.session  不仅可以做提交和回滚，还可以做查询
        filter 接收条件表达式 （  Wish.launched == False 是表达式
                                Wish.launched = False 是关键字参数）
        通过sqlalchemy做 mysql的in 查询

        """
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{"count": w[0], '"count': w[1]} for w in count_list]
        return count_list

    # 查找isbn号对应的书籍
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 最近的礼物
    # distinct 去重  前提需要分组(group_by)
    # order_by 排序
    # 链式调用 返回query
    # all，first 不属于子函数 属于触发语句  链式调用触发到all之后，就会生成sql语句执行查询
    # desc 倒序

    # 对象代表是一个实例  代表一个礼物  而在一个礼物里面获取多个礼物是不合适的
    # 将实例方法改为类方法比较合适
    # 类代表礼物这个事物  ，他是抽象，不是具体的 “一个”
    # 实例方法是和对象对应的
    @classmethod
    def recent(cls):
        recent_gift = Gift.query. \
            filter_by(launched=False). \
            group_by(Gift.isbn). \
            order_by(desc(Gift.create_time)). \
            limit(current_app.config['RECENT_BOOK_COUNT']). \
            distinct().all()
        return recent_gift

# 可以根据查询是否是意义的
# 有意义的查询，适合放在model里面  比如上面的recent---查询礼物
# 没有业务意义的（并没有可以提取出具体的业务意义的话）  可以放在视图函数中
# 有具体业务意义的代码尽量不要写在视图函数中
# 建立类 要有特征和行为
