from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_avatars import Avatars
from application.admin import AdminHomeView, AdminUserView, AdminPostView, AdminCommentView, AdminTagView
from flask_ckeditor import CKEditor
from flask_mail import Mail
import config

# Globally accessible variables
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = 'Sign in to access this page.'
login_manager.login_message_category = 'warning'
admin = Admin()
avatars = Avatars()
ckeditor = CKEditor()
mail = Mail()


def create_app(config_class=config.ProductionConfig):
    # App generation and configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Plugins initialization
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app, index_view=AdminHomeView())
    avatars.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    # Admin plugin
    from application.models import User, Post, Comment, Tag
    admin.add_view(AdminUserView(User, db.session))
    admin.add_view(AdminPostView(Post, db.session))
    admin.add_view(AdminCommentView(Comment, db.session))
    admin.add_view(AdminTagView(Tag, db.session))

    # Blueprints
    from application.main.views import main
    from application.auth.views import auth
    from application.users.views import users
    from application.posts.views import posts
    from application.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    # If SQLite is chosen database implement Foreign Keys.
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        @event.listens_for(Engine, "connect")
        def _sqlite_fk_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    return app
