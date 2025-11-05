# app/services/wechat.py
import httpx
import asyncio
import time
from typing import Dict, Optional, Any
from functools import wraps
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=3, delay=1.0):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = await func(*args, **kwargs)
                    if attempt > 0:
                        logger.info(f"第{attempt+1}次重试成功")
                    return result
                except Exception as e:
                    if attempt == max_retries - 1:  # 最后一次尝试
                        logger.error(f"所有重试失败: {str(e)}")
                        raise
                    logger.warning(
                        f"第{attempt+1}次尝试失败，{delay}秒后重试: {str(e)}"
                    )
                    await asyncio.sleep(delay * (attempt + 1))  # 指数退避
            return None

        return wrapper

    return decorator


class WeChatService:
    """增强版微信服务"""

    def __init__(self):
        self.app_id = settings.WECHAT_APP_ID
        self.app_secret = settings.WECHAT_APP_SECRET
        self.base_url = "https://api.weixin.qq.com"
        self._access_token_cache = None
        self._token_expire_time = 0
        self._client = None

    @property
    async def client(self):
        """获取或创建HTTP客户端（连接池复用）"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0),
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        return self._client

    @retry_on_failure(max_retries=3, delay=1.0)
    async def code2session(self, code: str) -> Dict[str, Any]:
        """
        - 自动重试机制
        - 参数验证
        - 智能错误处理
        """
        # 参数验证
        if not code or len(code) < 10:
            return {"errcode": 40029, "errmsg": "无效的授权码"}

        # 构建请求
        url = f"{self.base_url}/sns/jscode2session"
        params = {
            "appid": self.app_id,
            "secret": self.app_secret,
            "js_code": code,
            "grant_type": "authorization_code",
        }

        client = await self.client
        try:
            # 发送请求
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # 记录请求日志（脱敏处理）
            log_data = data.copy()
            if "openid" in log_data:
                log_data["openid"] = f"{log_data['openid'][:8]}..."  # 脱敏
            logger.info(f"微信登录响应: {log_data}")

            return data

        except httpx.TimeoutException:
            logger.error("微信API请求超时")
            return {"errcode": -1, "errmsg": "请求超时，请稍后重试"}
        except httpx.HTTPStatusError as e:
            logger.error(f"微信API HTTP错误: {e.response.status_code}")
            return {"errcode": -1, "errmsg": f"HTTP错误: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"微信登录未知错误: {str(e)}")
            return {"errcode": -1, "errmsg": "系统繁忙，请稍后重试"}

    async def get_access_token(self, force_refresh: bool = False) -> Optional[str]:
        """获取access_token（带缓存）"""
        current_time = time.time()

        # 检查缓存是否有效（提前5分钟刷新）
        if (
            not force_refresh
            and self._access_token_cache
            and current_time < self._token_expire_time - 300
        ):
            return self._access_token_cache

        url = f"{self.base_url}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }

        client = await self.client
        try:
            response = await client.get(url, params=params)
            data = response.json()

            if "access_token" in data:
                self._access_token_cache = data["access_token"]
                self._token_expire_time = current_time + data.get("expires_in", 7200)
                logger.info("成功获取微信access_token")
                return self._access_token_cache
            else:
                logger.error(f"获取access_token失败: {data}")
                return None

        except Exception as e:
            logger.error(f"获取access_token异常: {str(e)}")
            return None

    async def get_user_info(
        self, openid: str, access_token: str = None
    ) -> Dict[str, Any]:
        """获取用户基本信息（需要用户授权）"""
        if not access_token:
            access_token = await self.get_access_token()
            if not access_token:
                return {"errcode": -1, "errmsg": "获取access_token失败"}

        url = f"{self.base_url}/cgi-bin/user/info"
        params = {"access_token": access_token, "openid": openid, "lang": "zh_CN"}

        client = await self.client
        try:
            response = await client.get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return {"errcode": -1, "errmsg": str(e)}

    async def validate_signature(
        self, signature: str, timestamp: str, nonce: str, token: str
    ) -> bool:
        """验证微信消息签名"""
        try:
            import hashlib

            params = [token, timestamp, nonce]
            params.sort()
            sign = hashlib.sha1("".join(params).encode()).hexdigest()
            return sign == signature
        except Exception as e:
            logger.error(f"签名验证失败: {str(e)}")
            return False

    async def close(self):
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None


# 创建全局实例
wechat_service = WeChatService()

# 应用关闭时清理资源
import atexit


@atexit.register
def cleanup():
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(wechat_service.close())
    except:
        pass
