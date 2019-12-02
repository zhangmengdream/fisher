from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base


# 赠送此书
class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 这里gift对应的book  就使用isbn编号    （因为这个项目的book是在接口中获取而不是数据库中，所以无法用外键  换种思路）
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

