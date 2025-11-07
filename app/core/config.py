import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "奶茶店小程序后端"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = (
        "mysql+mysqldb://admin:Amazing0534@sh-cynosdbmysql-grp-08otnh8a.sql.tencentcdb.com:26106/cloud1-7g2z6qs0ef1cb4ae"
    )

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()

    return settings


# 全局配置实例
settings = get_settings()
