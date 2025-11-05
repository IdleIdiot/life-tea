import os
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
    DATABASE_URL: str = "mysql+mysqldb://user:password@localhost/milk_tea_shop"

    # 微信小程序配置
    # WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    # WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "")
    # WECHAT_TOKEN_URL: str = "https://api.weixin.qq.com/sns/jscode2session"

    # JWT 配置
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "your-secret-key-change-in-production"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()

    # 验证必要的配置
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY.startswith("your-"):
        print(settings.JWT_SECRET_KEY)
        logger.warning("JWT_SECRET_KEY未正确配置，使用默认值，生产环境请修改！")

    return settings


# 全局配置实例
settings = get_settings()
