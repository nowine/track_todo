import secrets
from pydantic import BaseSettings, PostgresDsn

'''
使用BaseSetting可以更好的管理系统配置。
继承自BaseSetting的类可以进一步定义配置字段的类型，默认值等信息。
同时，在生成配置实例的时候，可以传入key-value pair来初始化配置。
最后，如果没有传入初始化值，Setting类会尝试寻找环境变量来覆盖原有配置。
'''
class Settings(BaseSettings):
    #SQLALCHEMY_DATABASE_URL: PostgresDsn = "postgresql+psycopg2://pi:Nil0911@192.168.31.193:5432/track_todo"
    SQLALCHEMY_DATABASE_URL: PostgresDsn = "postgresql://pi:Nil0911@192.168.31.193:5432/track_todo"

    # Random string to be added to the original password for encryption
    SALT: str = 'jsfh2o2rad@#'
    # Secret key for token encoding
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # The default expiry time of the access token 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        case_sensitive = True
        env_prefix = 'TRACK_TODO_'


settings = Settings()
