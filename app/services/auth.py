from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings


class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.access_expire_minutes = 60 * 2  # 2小时
        self.refresh_expire_days = 7  # 7天

    def create_access_token(self, user_id: int) -> str:
        """创建访问令牌（2小时）"""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_expire_minutes
        )

        payload = {"sub": str(user_id), "exp": expire, "type": "access"}

        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def create_refresh_token(self, user_id: int) -> str:
        """创建刷新令牌（7天）"""
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_expire_days)

        payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}

        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str, token_type: str = "access") -> int:
        """验证令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            # 检查类型
            if payload.get("type") != token_type:
                return None

            return int(payload["sub"])
        except:
            return None

    def refresh_tokens(self, refresh_token: str) -> dict:
        """使用刷新令牌获取新令牌"""
        user_id = self.verify_token(refresh_token, "refresh")
        if not user_id:
            return None

        return {
            "access_token": self.create_access_token(user_id),
            "refresh_token": self.create_refresh_token(user_id),  # 可选：返回新刷新令牌
        }


auth_service = AuthService()
