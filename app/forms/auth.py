from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, AnyOf, Email, ValidationError

from app.models.user import User


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])



class RegisterForm(LoginForm):
    # email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    #
    # password = PasswordField(validators=[
    #     DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])
    #
    # nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    # 自定义验证器  以validate_ 开头  后面附加 对哪个参数做校验
    # 如果触发了ValidationError 错误信息 回进入form.errors 里面
    # validate_email定义完成之后是不需要加入validators数组里面的  因为根据函数名字 就已经知道  是对哪个字段进行验证的了
    def validate_email(self, field):
        # 对数据库进行查询
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        # 对数据库进行查询
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('昵称已存在')


class EmailForm(Form):
    email = StringField(validators=[DataRequired(),Length(5,64),Email(message='电子邮箱不符合规范')])



