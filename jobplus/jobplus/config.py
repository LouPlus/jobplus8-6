class BaseConfig:
    SERCET_KEY = 'AAA'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
}