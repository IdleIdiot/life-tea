from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session


class CRUDBase:
    def __init__(self, model):
        """
        初始化
        :param model: SQLAlchemy 模型类
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[Any]:
        """根据ID获取单条记录"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[Any]:
        """根据字段查询"""
        return db.query(self.model).filter(getattr(self.model, field) == value).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """获取多条记录（分页）"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all(self, db: Session) -> List[Any]:
        """获取所有记录"""
        return db.query(self.model).all()

    def create(self, db: Session, obj_data: Dict[str, Any]) -> Any:
        """
        创建新记录
        :param obj_data: 字典形式的数据
        """
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Any, update_data: Dict[str, Any]) -> Any:
        """
        更新记录
        :param db_obj: 数据库中的对象实例
        :param update_data: 要更新的字段字典
        """
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> bool:
        """删除记录"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

    def count(self, db: Session) -> int:
        """统计记录总数"""
        return db.query(self.model).count()

    def exists(self, db: Session, id: Any) -> bool:
        """检查记录是否存在"""
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def search(
        self, db: Session, field: str, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[Any]:
        """简单搜索（模糊匹配）"""
        return (
            db.query(self.model)
            .filter(getattr(self.model, field).like(f"%{keyword}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
