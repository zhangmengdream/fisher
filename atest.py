class MyResource:
    def __enter__(self):
        # 连接资源
        print('connect to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        print('close resource connection')
        # return False


    def query(self):
        print('query data')

try:

    with MyResource() as resource:
        1/0
        resource.query()
except:
    pass



