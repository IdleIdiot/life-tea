from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, Cart, CartItem


class OrderCRUD:
    """订单 CRUD 操作"""

    def __init__(self):
        self.model = Order

    def get(self, db: Session, order_id: int):
        """根据ID获取订单"""
        return db.query(self.model).filter(self.model.id == order_id).first()

    def get_by_order_no(self, db: Session, order_no: str):
        """根据订单号获取订单"""
        return db.query(self.model).filter(self.model.order_no == order_no).first()

    def get_user_orders(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ):
        """获取用户的订单列表"""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_orders(self, db: Session, user_id=None, status=None, skip=0, limit=100):
        """搜索订单"""
        query = db.query(self.model)

        if user_id is not None:
            query = query.filter(self.model.user_id == user_id)
        if status is not None:
            query = query.filter(self.model.order_status == status)

        return (
            query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()
        )

    def update_status(self, db: Session, order_id: int, status: int):
        """更新订单状态"""
        order = self.get(db, order_id)
        if order:
            order.order_status = status
            db.commit()
            db.refresh(order)
        return order


class OrderItemCRUD:
    """订单项 CRUD 操作"""

    def __init__(self):
        self.model = OrderItem

    def get_by_order(self, db: Session, order_no: str):
        """获取订单的所有订单项"""
        return db.query(self.model).filter(self.model.order_no == order_no).all()


class CartCRUD:
    """购物车 CRUD 操作"""

    def __init__(self):
        self.model = Cart

    def get_by_user(self, db: Session, user_id: int):
        """获取用户的购物车"""
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def create(self, db: Session, user_id: int):
        """为用户创建购物车"""
        cart = self.model(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    def get_or_create(self, db: Session, user_id: int):
        """获取或创建购物车"""
        cart = self.get_by_user(db, user_id)
        if not cart:
            cart = self.create(db, user_id)
        return cart


class CartItemCRUD:
    """购物车项 CRUD 操作"""

    def __init__(self):
        self.model = CartItem

    def get(self, db: Session, cart_item_id: int):
        """根据ID获取购物车项"""
        return db.query(self.model).filter(self.model.id == cart_item_id).first()

    def get_by_cart(self, db: Session, cart_id: int):
        """获取购物车的所有商品"""
        return db.query(self.model).filter(self.model.cart_id == cart_id).all()

    def get_by_user_product(
        self, db: Session, user_id: int, product_id: int, specs: list
    ):
        """根据用户、商品和规格获取购物车项"""
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            return None

        return (
            db.query(self.model)
            .filter(
                self.model.cart_id == cart.id,
                self.model.product_id == product_id,
                self.model.selected_specs == specs,
            )
            .first()
        )

    def add_item(
        self, db: Session, cart_id: int, product_id: int, specs: list, quantity: int
    ):
        """添加商品到购物车"""
        # 检查是否已存在
        existing = (
            db.query(self.model)
            .filter(
                self.model.cart_id == cart_id,
                self.model.product_id == product_id,
                self.model.selected_specs == specs,
            )
            .first()
        )

        if existing:
            # 已存在，更新数量
            existing.quantity += quantity
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # 新增
            item = self.model(
                cart_id=cart_id,
                product_id=product_id,
                selected_specs=specs,
                quantity=quantity,
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item

    def update_quantity(self, db: Session, cart_item_id: int, quantity: int):
        """更新购物车项数量"""
        item = self.get(db, cart_item_id)
        if item:
            item.quantity = quantity
            db.commit()
            db.refresh(item)
        return item

    def remove_item(self, db: Session, cart_item_id: int):
        """从购物车移除商品"""
        item = self.get(db, cart_item_id)
        if item:
            db.delete(item)
            db.commit()
            return True
        return False

    def clear_cart(self, db: Session, cart_id: int):
        """清空购物车"""
        db.query(self.model).filter(self.model.cart_id == cart_id).delete()
        db.commit()


# 创建实例
order_crud = OrderCRUD()
order_item_crud = OrderItemCRUD()
cart_crud = CartCRUD()
cart_item_crud = CartItemCRUD()
