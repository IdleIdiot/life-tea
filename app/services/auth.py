from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self, user_id: int, expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建 JWT Token"""
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self.access_token_expire_minutes)
        )

        payload = {
            "sub": str(user_id),  # 标准做法：subject 存放用户ID
            "exp": expire,
            "iat": datetime.now(timezone.utc),  # 签发时间
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        """验证 JWT Token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # 检查是否过期（使用时区感知的时间比较）
            if datetime.now(timezone.utc) > datetime.fromtimestamp(
                payload["exp"], tz=timezone.utc
            ):
                return None

            return payload
        except JWTError:
            return None

    def get_user_id_from_token(self, token: str) -> Optional[int]:
        """从Token中提取用户ID"""
        payload = self.verify_token(token)
        if payload and "sub" in payload:
            try:
                return int(payload["sub"])
            except (ValueError, TypeError):
                return None
        return None

    def get_password_hash(self, password: str) -> str:
        """生成密码哈希"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)


# 创建全局实例
auth_service = AuthService()
