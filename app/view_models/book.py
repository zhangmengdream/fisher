# 1 统一结构
# 2 集合

# 处理单本的数据
class BookViewModel:

    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages']
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.image = book['image']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


# 处理集合类的数据
class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    """
        data 原始数据
    """

    # 单本书
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    # 多本书
    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = len(data['books'])
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    # 裁剪数据
    @classmethod
    def __cut_book_data(cls, data):

        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'] or '',
            'summary': data['summary'],
            'image': data['image'],
        }
        return book
