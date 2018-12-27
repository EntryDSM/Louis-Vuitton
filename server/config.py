import os
import datetime


class Config:
    SERVICE_NAME = "entry_dsm"
    DOMAIN = None

    SECRET_KEY = os.getenv("SECRET_KEY", "fk30dk3ivnrodjfjfhjbirodkdlxmcmfjfjeoejvkeofr")

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=150)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=300)

    RUN_SETTINGS = {
        'threaded': True
    }


class DevConfig(Config):
    HOST = "localhost"
    PORT = 5000
    DEBUG = True

    RUN_SETTINGS = dict(Config.RUN_SETTINGS, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/{}".format(Config.SERVICE_NAME)


class ProductionConfig(Config):
    HOST = "entry.entrytdsm.hs.kr"
    PORT = 80
    DEBUG = False

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=5)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)

    RUN_SETTINGS = dict(Config.RUN_SETTINGS, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })


class TestConfig(DevConfig):
    TESTING = True
