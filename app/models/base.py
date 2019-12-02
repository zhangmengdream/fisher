from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 这里主要解决status
# 因为每次查询都需要使用status=1 也就是没被删除状态下的图书，所以这边在源码中强制加上status=1 条件，以后查询的时候，就不必再写了
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        # 当查询语句没有加status参数的时候  加1
        # 这里实现了自己的逻辑
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1

        # 这里加上了原有的filter_by 的逻辑
        # **kwargs 加两个星号是对字典进行解包
        # 调用基类下面的 filter_by 方法， 保存原有的
        return super(Query,self).filter_by(**kwargs)


# query_class 允许自己继承 basequery
db = SQLAlchemy(query_class=Query)


# 基类模型 让每个子模型继承这个基类模型  里面写相同的属性

class Base(db.Model):
    __abstract__ = True  # 作用  不让base生成表
    create_time = Column('create_time', Integer)
    # 软删除   通过改变shatus的状态 来控制这条数据是否被删除   1表示存在
    status = Column(SmallInteger, default=1)

    # 通用方法
    def set_attrs(self, attrs_dict):

        for key, value in attrs_dict.items():
            # 判断当前key在模型中 是否有同名属性  hasattr（判断对象，是否包含某个属性）
            if hasattr(self, key) and key != 'id':
                # 赋值
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None