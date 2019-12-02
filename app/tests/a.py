# from contextlib import contextmanager
#
# # contextmanager 装饰器
#
#
# def mank_myresource():
#     pass
#
#
#
#
kwargs = {1:'a',2:'b',3:'c'}
clauses = [key == value for key, value in kwargs.items()]
print(clauses)