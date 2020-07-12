import os

# Set Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG"]
    MAX_IMAGE_FILESIZE = 1 * 1024 * 1024

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    THREADED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    THREADED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True


class HerokuConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
