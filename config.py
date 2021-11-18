import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ADMIN_SWATCH = 'flatly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_PKG_TYPE = 'full'

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Recaptcha
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    # Pagination
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
    LOG_TO_STDOUT = True
