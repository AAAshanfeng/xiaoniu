# 小牛电商接口测试用例文档

被测对象：小牛电商测试实战系统 API<br>
API地址：http://43.133.227.52/api<br>
测试类型：接口功能测试 + 权限测试

## 1. 登录模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| login_001 | 登录成功 | 登录 | P0 | POST | {协议名+域名}/login | Content-Type:application/json | username："tester"<br>password："123456" | 返回code=0，提示“success”，返回token |
| login_002 | 密码错误 | 登录 | P1 | POST | {协议名+域名}/login | Content-Type:application/json | username："tester"<br>password："wrong_password" | 返回code=401，提示“账号或密码错误” |
| login_003 | 用户不存在 | 登录 | P1 | POST | {协议名+域名}/login | Content-Type:application/json | username："wrong_username"<br>password："123456" | 返回code=401，提示“账号或密码错误” |
| login_004 | 密码为空 | 登录 | P1 | POST | {协议名+域名}/login | Content-Type:application/json | username："tester"<br>password："" | 返回code=401，提示“账号或密码错误” |
| login_005 | 用户名为空 | 登录 | P1 | POST | {协议名+域名}/login | Content-Type:application/json | username：""<br>password："123456" | 返回code=401，提示“账号或密码错误” |
| login_006 | 密码字段不存在 | 登录 | P2 | POST | {协议名+域名}/login | Content-Type:application/json | username："tester" | 返回code=401，提示“账号或密码错误” |
| login_007 | 用户名类型错误 | 登录 | P2 | POST | {协议名+域名}/login | Content-Type:application/json | username：123456<br>password："123456" | 返回code=401，提示“账号或密码错误” |
| login_008 | 密码类型错误 | 登录 | P2 | POST | {协议名+域名}/login | Content-Type:application/json | username："tester"<br>password：123456 | 返回code=401，提示“账号或密码错误” |

---

## 2. 商品列表模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| products_001 | 登录后获取商品列表 | 商品列表 | P0 | GET | {协议名+域名}/products | Authorization: Bearer {{token}} | 空 | 返回code=0，提示“success”，返回商品列表 |
| products_002 | 未登录获取商品列表 | 商品列表 | P1 | GET | {协议名+域名}/products | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |
| products_003 | 商品列表数据校验 | 商品列表 | P1 | GET | {协议名+域名}/products | Authorization: Bearer {{token}} | 空 | 商品字段包含 id、name、price、stock，数据正确 |

---

## 3. 查询购物车模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| check_cart_001 | 正常查询购物车 | 购物车 | P0 | GET | {协议名+域名}/cart | Authorization: Bearer {{token}} | 空 | 返回code=0，提示“success”，返回购物车列表 |
| check_cart_002 | 未登录查询购物车 | 购物车 | P1 | GET | {协议名+域名}/cart | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |
| check_cart_003 | 购物车商品数据校验 | 购物车 | P1 | GET | {协议名+域名}/cart | Authorization: Bearer {{token}} | 空 | items 存在且商品信息正确、totalAmount正确，等于购物车商品金额之和 |

---

## 4. 加入购物车模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|--|---|
| add_cart_001 | 正常加入购物车 | 购物车 | P0 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：101<br>quantity：1 | 返回code=0，提示“success” |
| add_cart_002 | 重复加入同一商品 | 购物车 | P1 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：101<br>quantity：1 | 返回code=0，提示“success” |
| add_cart_003 | quantity为0 | 购物车 | P1 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：101<br>quantity：0 | 加入失败，返回参数错误 |
| add_cart_004 | quantity为负数 | 购物车 | P2 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：101<br>quantity：-1 | 加入失败，返回参数错误 |
| add_cart_005 | quantity过大 | 购物车 | P2 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：101<br>quantity：100 | 加入失败，返回参数错误 |
| add_cart_006 | 不存在的productId | 购物车 | P1 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：0<br>quantity：1 | 加入失败，提示商品不存在 |
| add_cart_007 | 库存为0的商品 | 购物车 | P1 | POST | {协议名+域名}/cart | Authorization: Bearer {{token}} | productId：104<br>quantity：1 | 加入失败，提示库存不足 |
| add_cart_008 | 未登录加入购物车 | 购物车 | P1 | POST | {协议名+域名}/cart | 空 | productId：101<br>quantity：1 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

###  已发现问题 —— add_cart_003

- **实际结果**：传入 quantity=0 时，接口仍然返回 code=0，并且购物车商品数量增加 1 个。
- **状态**：不通过，多次验证复现
- **说明**：预期应该拒绝 quantity=0 的请求并返回参数错误，但实际接口将其当成正常添加商品处理。

### 已发现问题 —— add_cart_005

- **实际结果**：传入 quantity=100 时，接口返回 code=0，并且购物车商品数量直接增加 100 个。
- **状态**：不通过，稳定复现
- **问题说明**：预期应该对商品数量进行合理的参数校验，但实际接口允许一次加入 100 个商品。

------

## 5. 删除购物车商品模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| delete_cart_001 | 删除存在商品 | 购物车 | P0 | DELETE | {协议名+域名}/cart/101 | Authorization: Bearer {{token}} | 空 | 返回code=0，删除成功 |
| delete_cart_002 | 删除不存在商品 | 购物车 | P1 | DELETE | {协议名+域名}/cart/9999 | Authorization: Bearer {{token}} | 空 | 删除失败，不影响现有购物车 |
| delete_cart_003 | 检查购物车数据是否更新 | 购物车 | P1 | DELETE | {协议名+域名}/cart/101 | Authorization: Bearer {{token}} | 空 | 商品数量减少/商品消失，总金额正确更新 |
| delete_cart_004 | 未登录删除商品 | 购物车 | P2 | DELETE | {协议名+域名}/cart/101 | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

### 已发现问题 —— delete_cart_002

- **实际结果**：删除不存在的商品时，接口返回 `code=0`，并返回购物车列表。
- **状态**：疑似问题
- **问题说明**：预期是“删除失败，不影响现有购物车”，但实际返回成功码。由于返回的购物车数据与原来一致，核心数据没有受到影响，因此主要问题在于**接口对异常操作的返回状态不够准确**。

------

## 6. 创建订单模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| create_orders_001 | 购物车有商品时创建订单 | 订单 | P0 | POST | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 返回code=0，创建成功，返回订单信息 |
| create_orders_002 | 购物车为空时创建订单 | 订单 | P1 | POST | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 创建失败，返回合理提示，不生成无商品订单 |
| create_orders_003 | 检查创建订单后购物车是否清空 | 订单 | P2 | POST | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 购物车为空 |
| create_orders_004 | 检查商品库存是否扣减 | 订单 | P2 | POST | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 库存按照购买数量正确扣减 |
| create_orders_005 | 检查订单金额是否等于商品小计之和 | 订单 | P2 | POST | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 订单总金额 = 各商品小计之和 |
| create_orders_006 | 未登录创建订单 | 订单 | P2 | POST | {协议名+域名}/orders | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

---

## 7. 查询订单列表模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| check_orders_001 | 查询当前用户订单 | 订单 | P0 | GET | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 返回code=0，返回当前用户的订单列表 |
| check_orders_002 | 新订单是否排在前面 | 订单 | P1 | GET | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 最新创建的订单排在前面 |
| check_orders_003 | 订单状态文案是否正确 | 订单 | P1 | GET | {协议名+域名}/orders | Authorization: Bearer {{token}} | 空 | 返回的状态文案与实际订单状态一致 |
| check_orders_004 | 未登录查询用户订单 | 订单 | P2 | GET | {协议名+域名}/orders | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

---

## 8. 查询订单详情模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| check_orders_001 | 查询存在订单 | 订单 | P0 | GET | {协议名+域名}/orders/NO13510 | Authorization: Bearer {{token}} | 空 | 返回code=0，返回该订单的详细信息 |
| check_orders_002 | 查询不存在订单 | 订单 | P1 | GET | {协议名+域名}/orders/NO99999 | Authorization: Bearer {{token}} | 空 | 查询失败，返回合理的错误提示 |
| check_orders_003 | 查询其他用户订单 | 订单 | P1 | GET | {协议名+域名}/orders/NO13510 | Authorization: Bearer {{token}} | 空 | 查询失败，不允许查看其他用户订单 |
| check_orders_004 | 未登录查询订单下详情 | 订单 | P2 | GET | {协议名+域名}/orders/NO13510 | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

---

## 9. 支付订单模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| pay_orders_001 | 支付待支付订单 | 订单 | P0 | POST | {协议名+域名}/orders/NO13510/pay | Authorization: Bearer {{token}} | 空 | 返回code=0，支付成功，订单状态变为已支付 |
| pay_orders_002 | 支付已取消订单 | 订单 | P1 | POST | {协议名+域名}/orders/NO13512/pay | Authorization: Bearer {{token}} | 空 | 支付失败，订单状态保持已取消 |
| pay_orders_003 | 支付不存在订单 | 订单 | P1 | POST | {协议名+域名}/orders/NO99999/pay | Authorization: Bearer {{token}} | 空 | 支付失败，返回合理错误提示 |
| pay_orders_004 | 重复支付订单 | 订单 | P2 | POST | {协议名+域名}/orders/NO13507/pay | Authorization: Bearer {{token}} | 空 | 支付失败或提示订单已支付，不应重复支付 |
| pay_orders_005 | 未登录支付订单 | 订单 | P2 | POST | {协议名+域名}/orders/NO13510/pay | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

### 已发现问题 —— pay_orders_004

- **实际结果**：对已经支付的订单再次发起支付请求，接口返回 code=0，返回该订单的详细信息。
- **状态**：不通过，存在业务逻辑问题
- **问题说明**：预期应该拒绝重复支付或明确提示订单已经支付，但实际接口仍返回成功状态。

------

## 10. 取消订单模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| cancel_orders_001 | 取消待支付订单 | 订单 | P0 | POST | {协议名+域名}/orders/NO13509/cancel | Authorization: Bearer {{token}} | 空 | 返回code=0，取消成功，订单状态变为已取消 |
| cancel_orders_002 | 取消已支付订单 | 订单 | P1 | POST | {协议名+域名}/orders/NO13510/cancel | Authorization: Bearer {{token}} | 空 | 取消失败，订单状态保持已支付 |
| cancel_orders_003 | 取消不存在订单 | 订单 | P1 | POST | {协议名+域名}/orders/NO99999/cancel | Authorization: Bearer {{token}} | 空 | 取消失败，返回合理错误提示 |
| cancel_orders_004 | 取消已取消订单 | 订单 | P2 | POST | {协议名+域名}/orders/NO13512/cancel | Authorization: Bearer {{token}} | 空 | 取消失败，订单状态保持已取消 |
| cancel_orders_005 | 未登录取消订单 | 订单 | P2 | POST | {协议名+域名}/orders/NO13510/cancel | 空 | 空 | 返回code=401，提示“请先登录，或检查 token 是否正确” |

### 已发现问题 —— cancel_orders_004

- **实际结果**：对已经取消的订单再次执行取消操作，接口返回 code=0，返回订单详细信息，订单状态仍保持“已取消”。
- **状态**：疑似问题
- **问题说明**：预期是取消失败，但实际返回 code=0。虽然订单状态没有被错误修改，但接口返回状态与预期不一致。

------

## 11. 重置练习数据模块

| 用例编号 | 用例标题 | 模块 | 优先级 | 请求方法 | URL | 请求头 | 请求体（请求数据） | 预期结果 |
|---|---|---|---|---|---|---|---|---|
| reset_001 | 普通用户重置练习数据 | 重置 | P1 | POST | {协议名+域名}/reset | Authorization: Bearer {{token}} | 空 | 返回code=403，数据不被重置 |
| reset_002 | 管理员重置练习数据 | 重置 | P0 | POST | {协议名+域名}/reset | Authorization: Bearer {{b_token}} | 空 | 返回code=0，重置成功，返回成功信息 |
| reset_003 | 重置后订单、购物车、库存恢复 | 重置 | P1 | POST | {协议名+域名}/reset | Authorization: Bearer {{b_token}} | 空 | 订单、购物车、库存是否恢复初始状态 |

---
