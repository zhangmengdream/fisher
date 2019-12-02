from flask import Flask
# from app.models.book import db
from app.models.base import db
from flask_login import LoginManager

# 实例化
login_manager = LoginManager()

# 初始化
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.config')
    app.config.from_object('app.secure')
    register_blueprints(app)
    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprints(app):
    from app.web.book import web
    from app.web.user import user
    app.register_blueprint(web)
    app.register_blueprint(user)
