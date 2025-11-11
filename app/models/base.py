from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import declarative_base, class_mapper

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    # def to_dict(self, exclude_none=False, exclude_fields=None):
    #     """
    #     将模型实例转换为字典

    #     Args:
    #         exclude_none: 是否排除值为None的字段
    #         exclude_fields: 要排除的字段列表
    #     """
    #     if exclude_fields is None:
    #         exclude_fields = []

    #     result = {}

    #     # 获取所有列信息
    #     columns = class_mapper(self.__class__).columns

    #     for column in columns:
    #         # 跳过排除的字段
    #         if column.name in exclude_fields:
    #             continue

    #         value = getattr(self, column.name)

    #         # 如果排除None值且当前值为None，则跳过
    #         if exclude_none and value is None:
    #             continue

    #         # 处理datetime对象，转换为字符串
    #         # if isinstance(value, datetime):
    #         #     result[column.name] = value.isoformat()
    #         # else:
    #         result[column.name] = value

    #     return result
