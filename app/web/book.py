from flask import jsonify, Blueprint, request, current_app, make_response, flash, render_template
from flask_login import current_user
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import Trade_Info
from yushu_book import YuShuBook
from . import web


# x = current_app.config['DEBUG']


# 搜索图书（按姓名，书名，isbn...）
@web.route('/book/search/', endpoint='search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)
        books.fill(yushu_book, q)
        # 将对象序列化成字典  lambda  将对象内的对象序列化成字典

        # return json.dumps(books, default=lambda o: o.__dict__)

    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)

    # headers = {}
    # response = make_response('result',200)
    # response['headers'] =headers
    # return response


@web.route('/index')
def index():
    return 'web/index'


@web.route('/my_wish')
def my_wish():
    return 'web/my_wish'


@web.route('/pending')
def pending():
    return 'web/pending'


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 默认情况下 一本图书 既不再心愿清单 也不在礼物清单
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍的详细数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 这里处理用户登录的情况  如果用户没有登录，这里不需要做任何处理
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    # 首先把所有赠送者和所有索要者的清单查询出来
    # 然后根据具体的变量取值，显示出具体的响应控制
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Gift.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = Trade_Info(trade_gifts)
    trade_wishes_model = Trade_Info(trade_wishes)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
