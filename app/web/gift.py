from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from . import web
from flask_login import login_required, current_user
from flask import current_app, flash, redirect, url_for


@web.route('/my_gifts')
@login_required  # 装饰登录后才能访问的接口
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    # 获取我的礼物的isbn列表
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)



    return wish_count_list


# current_user (就是实例化后的User的模型)获取当前用户的相关信息
# 赠送此书
@web.route('/gift/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务  回滚
        # 如果数据执行到 commit时出现了错误就一定要执行rollback 回滚 ，否则后面的commit都会出错
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)

    else:
        flash('这本书已经添至心愿清单或赠送清单 请不要重复添加')


    return redirect(url_for('gifts.html'))


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务  回滚
        # 如果数据执行到 commit时出现了错误就一定要执行rollback 回滚 ，否则后面的commit都会出错
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已经添至心愿清单或赠送清单 请不要重复添加')
    return redirect(url_for('web.book_detail',isbn=isbn))









