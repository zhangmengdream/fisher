from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import logout_user, login_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        # form.data 包含了客户端提交过来的所有参数
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        # url_for  接收一个endpoint
        redirect(url_for('web.login'))
    return render_template('auth/register.html', form={'data': {}})


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        # 首先把用户的信息查询出来
        user = User.query.filter_by(email=form.email.data).first()
        # 需要把用户传进来的明文密码加密之后  在与数据库中的密码进行比较
        if user and user.check_password(form.password.data):
            # 用户身份通过之后 使用 logout_user保存用户票据  （存储cookie）
            # remember = True 记住状态  默认365天   如果想更改过期时间  就在config里面加上配置
            # 配置自己定义的过期时间  REMEMBER_COOKIE_DURATION
            login_user(user, remember=True)
        else:
            flash('用户不存在或密码错误')
    return render_template('auth/login.html', form={'data': {}})


@web.route('/logout')
def logout():
    logout_user() # 实现的是清空cookie的过程
    return redirect(url_for('web.index'))

# 忘记密码
@web.route('/reset/password',methods=['GET','POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email = account_email).first_or_404()
            if user:

                pass


    return render_template('auth/forget_password_request.html',form=form)






