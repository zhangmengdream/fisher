from flask import jsonify, Blueprint
from app.libs.helper import is_isbn_or_key
from yushu_book import YuShuBook

user = Blueprint('user', __name__)


# 搜索图书（按姓名，书名，isbn...）
@user.route('/book/search/<q>/<page>')
def search(q, page):
    isbn_or_key = is_isbn_or_key(q)
    result = YuShuBook.search_by_isbn(q) if isbn_or_key == 'isbn' else YuShuBook.search_by_keyword(q)
    return jsonify(result)
