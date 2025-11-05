### 数据表详细设计

以下是每个表的字段详细说明。

#### 1. 用户表 (`users`)
存储小程序用户的基本信息，通常与微信开放平台用户体系打通。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `openid` | VARCHAR | 64 | NOT | - | 微信用户唯一标识 |
| `unionid` | VARCHAR | 64 | YES | - | 微信开放平台统一ID |
| `nick_name` | VARCHAR | 100 | YES | - | 用户昵称 |
| `avatar_url` | VARCHAR | 255 | YES | - | 头像URL |
| `phone` | VARCHAR | 20 | YES | - | 手机号 |
| `gender` | TINYINT | - | YES | 0 | 性别 (0:未知, 1:男, 2:女) |
| `birthday` | DATE | - | YES | - | 生日 |
| `member_level` | TINYINT | - | YES | 1 | 会员等级 (1: 普通, 2: VIP, 3: SVIP) |
| `points` | INT | - | YES | 0 | 积分 |
| `status` | TINYINT | - | YES | 1 | 状态 (1:正常, 0:禁用) |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | - | YES | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：**
- 主键：`id`
- 唯一索引：`uk_openid` (`openid`)
- 普通索引：`idx_phone` (`phone`)

---

#### 2. 用户地址表 (`user_addresses`)
存储用户的收货地址（对于支持外卖的店铺）。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `user_id` | BIGINT | - | NOT | - | **外键**，关联 `users.id` |
| `contact_name` | VARCHAR | 50 | NOT | - | 收货人姓名 |
| `contact_phone` | VARCHAR | 20 | NOT | - | 收货人电话 |
| `region` | VARCHAR | 255 | NOT | - | 省市区（如：广东省深圳市南山区） |
| `address_detail` | VARCHAR | 255 | NOT | - | 详细地址 |
| `latitude` | DECIMAL | (10, 6) | YES | - | 纬度（用于距离计算） |
| `longitude` | DECIMAL | (10, 6) | YES | - | 经度（用于距离计算） |
| `is_default` | TINYINT | - | YES | 0 | 是否默认地址 (1:是, 0:否) |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | - | YES | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：**
- 主键：`id`
- 普通索引：`idx_user_id` (`user_id`)

---

#### 3. 商品分类表 (`categories`)
用于管理菜单分类，如“经典奶茶”、“水果茶”、“咖啡”等。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INT | - | NOT | AUTO_INCREMENT | **主键** |
| `name` | VARCHAR | 50 | NOT | - | 分类名称 |
| `description` | VARCHAR | 255 | YES | - | 分类描述 |
| `image_url` | VARCHAR | 255 | YES | - | 分类图片 |
| `sort_order` | INT | - | YES | 0 | 排序权重（数字越大越靠前） |
| `status` | TINYINT | - | YES | 1 | 状态 (1:显示, 0:隐藏) |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |

**索引：**
- 主键：`id`

---

#### 4. 商品（饮品）表 (`products`)
存储所有饮品/商品的核心信息。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INT | - | NOT | AUTO_INCREMENT | **主键** |
| `category_id` | INT | - | NOT | - | **外键**，关联 `categories.id` |
| `name` | VARCHAR | 100 | NOT | - | 商品名称（如：珍珠奶茶） |
| `description` | TEXT | - | YES | - | 商品描述 |
| `main_image` | VARCHAR | 255 | NOT | - | 主图URL |
| `image_list` | JSON | - | YES | - | 轮播图URL数组 |
| `base_price` | DECIMAL | (10, 2) | NOT | - | **基础价格**（小杯价格） |
| `is_hot` | TINYINT | - | YES | 0 | 是否热门推荐 (1:是, 0:否) |
| `is_new` | TINYINT | - | YES | 0 | 是否新品 (1:是, 0:否) |
| `sales_volume` | INT | - | YES | 0 | 总销量 |
| `month_sales` | INT | - | YES | 0 | 月销量 |
| `stock` | INT | - | YES | 999 | 库存（-1表示无限） |
| `status` | TINYINT | - | YES | 1 | 状态 (1:上架, 0:下架) |
| `sort_order` | INT | - | YES | 0 | 排序 |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |

**索引：**
- 主键：`id`
- 普通索引：`idx_category_id` (`category_id`), `idx_status` (`status`)

---

#### 5. 商品规格表 (`product_specs`)
**核心表**：用于管理饮品的规格（如杯型、温度、甜度、加料）及其对应的价格增量。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INT | - | NOT | AUTO_INCREMENT | **主键** |
| `product_id` | INT | - | NOT | - | **外键**，关联 `products.id` |
| `spec_type` | TINYINT | - | NOT | - | **规格类型** (1:杯型, 2:温度, 3:甜度, 4:加料) |
| `spec_name` | VARCHAR | 50 | NOT | - | 规格名称（如：大杯， 去冰， 半糖， 珍珠） |
| `additional_price` | DECIMAL | (8, 2) | YES | 0.00 | **附加价格**（在基础价格上增加） |
| `stock` | INT | - | YES | 999 | 该规格库存（-1表示无限） |
| `is_default` | TINYINT | - | YES | 0 | 是否默认选项 (1:是, 0:否) |
| `status` | TINYINT | - | YES | 1 | 状态 (1:可用, 0:不可用) |
| `sort_order` | INT | - | YES | 0 | 排序 |

**索引：**
- 主键：`id`
- 普通索引：`idx_product_id` (`product_id`), `idx_spec_type` (`spec_type`)

---

#### 6. 购物车表 (`carts`) 和 购物车项表 (`cart_items`)
采用主从表结构，因为一个用户的购物车可能包含多个商品。

**主表 `carts`**：每个用户只有一个购物车。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `user_id` | BIGINT | - | NOT | - | **外键**，关联 `users.id` |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | - | YES | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |


**从表 `cart_items`**：存储购物车中的具体商品和选择的规格。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `cart_id` | BIGINT | - | NOT | - | **外键**，关联 `carts.id` |
| `product_id` | INT | - | NOT | - | **外键**，关联 `products.id` |
| `quantity` | INT | - | NOT | 1 | 商品数量 |
| `selected_specs` | JSON | - | NOT | - | **JSON数组，存储用户选择的规格ID** <br> 例如：`[201, 205, 210]` (代表大杯，去冰，珍珠) |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 创建时间 |

**索引：**
- `cart_items` 表：`idx_cart_id` (`cart_id`), `idx_product_id` (`product_id`)

---

#### 7. 订单表 (`orders`) 和 订单项表 (`order_items`)
核心业务表，记录每一笔交易。
**主表 `orders`**：订单概要信息。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_no` | VARCHAR | 32 | NOT | - | **主键**，订单号（系统生成，如`20241105123456`） |
| `user_id` | BIGINT | - | NOT | - | **外键**，关联 `users.id` |
| `order_amount` | DECIMAL | (10, 2) | NOT | - | 订单总金额 |
| `discount_amount` | DECIMAL | (10, 2) | YES | 0.00 | 优惠金额（优惠券等） |
| `actual_amount` | DECIMAL | (10, 2) | NOT | - | 实付金额 |
| `payment_method` | TINYINT | - | YES | - | 支付方式 (1:微信支付, 2:余额, 3:到店付) |
| `payment_status` | TINYINT | - | YES | 0 | 支付状态 (0:待支付, 1:已支付, 2:已退款) |
| `order_status` | TINYINT | - | YES | 0 | 订单状态 (0:待接单, 1:制作中, 2:待取餐, 3:已完成, -1:已取消) |
| `pickup_method` | TINYINT | - | YES | 1 | 取餐方式 (1:到店自取, 2:外卖配送) |
| `pickup_code` | VARCHAR | 10 | YES | - | 取餐码（如：A102） |
| `remarks` | VARCHAR | 255 | YES | - | 用户备注 |
| `estimated_time` | DATETIME | - | YES | - | 预计完成时间 |
| `created_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 下单时间 |

**从表 `order_items`**：订单中包含的具体商品详情。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `order_no` | VARCHAR | 32 | NOT | - | **外键**，关联 `orders.order_no` |
| `product_id` | INT | - | NOT | - | **外键**，关联 `products.id` |
| `product_name` | VARCHAR | 100 | NOT | - | 商品快照名称（如：珍珠奶茶） |
| `product_image` | VARCHAR | 255 | NOT | - | 商品快照图片 |
| `unit_price` | DECIMAL | (8, 2) | NOT | - | 该商品项的单价 |
| `quantity` | INT | - | NOT | 1 | 数量 |
| `spec_description` | VARCHAR | 255 | YES | - | 规格文本快照（如：大杯, 去冰, 半糖, 加珍珠） |
| `selected_specs_json` | JSON | - | YES | - | 选择的规格ID JSON快照 |

**索引：**
- `orders` 表：`idx_user_id` (`user_id`), `idx_created_at` (`created_at`)
- `order_items` 表：`idx_order_no` (`order_no`)

---

#### 8. 优惠券/活动表 (`coupons`) 和 用户优惠券表 (`user_coupons`)
管理营销活动。
**主表 `coupons`**：定义优惠券模板。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INT | - | NOT | AUTO_INCREMENT | **主键** |
| `name` | VARCHAR | 100 | NOT | - | 优惠券名称 |
| `type` | TINYINT | - | NOT | - | 类型 (1:满减券, 2:折扣券) |
| `discount_value` | DECIMAL | (10, 2) | NOT | - | 优惠值（满减金额或折扣，如8折存0.8） |
| `min_amount` | DECIMAL | (10, 2) | YES | - | 最低消费金额 |
| `status` | TINYINT | - | YES | 1 | 状态 (1:有效, 0:无效) |
| `total_count` | INT | - | YES | -1 | 发放总量（-1不限量） |
| `claimed_count` | INT | - | YES | 0 | 已领取量 |
| `validity_type` | TINYINT | - | NOT | - | 有效期类型 (1:固定日期, 2:领取后生效) |
| `start_time` | DATETIME | - | YES | - | 开始时间 |
| `end_time` | DATETIME | - | YES | - | 结束时间 |
| `valid_days` | INT | - | YES | - | 有效天数（ validity_type=2 时用） |

**从表 `user_coupons`**：记录用户领取和使用的每一张券。
| 字段名 | 类型 | 长度 | 可空 | 默认值 | 注释 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | - | NOT | AUTO_INCREMENT | **主键** |
| `user_id` | BIGINT | - | NOT | - | **外键**，关联 `users.id` |
| `coupon_id` | INT | - | NOT | - | **外键**，关联 `coupons.id` |
| `status` | TINYINT | - | YES | 0 | 状态 (0:未使用, 1:已使用, 2:已过期) |
| `used_order_no` | VARCHAR | 32 | YES | - | 使用的订单号，关联 `orders.order_no` |
| `claimed_at` | DATETIME | - | YES | CURRENT_TIMESTAMP | 领取时间 |
| `used_at` | DATETIME | - | YES | - | 使用时间 |
| `expire_at` | DATETIME | - | NOT | - | 过期时间 |

**索引：**
- `user_coupons` 表：`idx_user_id` (`user_id`), `idx_status` (`status`), `idx_expire_at` (`expire_at`)

---

### 设计思路总结

1.  **灵活性**：`product_specs` 表的设计是核心，它将杯型、温度、甜度、加料等属性统一管理，极大增强了商品配置的灵活性，无需为每种组合单独建商品。
2.  **可扩展性**：表结构考虑了外卖、会员积分、多种营销活动等场景，预留了扩展空间。`image_list`、`selected_specs` 等字段使用 JSON 类型，避免了过度范式化带来的复杂性。
3.  **数据一致性**：通过外键约束（如果数据库引擎支持）和应用程序逻辑保证数据完整性。订单相关表使用了快照技术，确保订单历史数据不受后续商品信息变更的影响。
4.  **性能**：为常用的查询字段（如用户ID、订单时间、状态等）建立了索引，以保证查询效率。