def test_create_and_pay_order(api, user_header):
    """创建订单并支付"""

    add_cart_response = api.add_cart(102, 1, user_header)
    assert add_cart_response.status_code == 200
    assert add_cart_response.json()["code"] == 0
    assert add_cart_response.json()["items"][0]["productId"] == 102

    create_orders_response = api.create_order(user_header)
    assert create_orders_response.status_code == 200
    assert create_orders_response.json()["code"] == 0
    assert create_orders_response.json()["order"]["statusText"] == "待支付"
    orderId = create_orders_response.json()["order"]["id"]

    pay_orders_response = api.pay_order(orderId, user_header)
    assert pay_orders_response.status_code == 200
    assert pay_orders_response.json()["code"] == 0
    assert pay_orders_response.json()["order"]["statusText"] == "已支付"

    check_order_response = api.check_detail_order(orderId, user_header)
    assert check_order_response.status_code == 200
    assert check_order_response.json()["code"] == 0
    assert check_order_response.json()["order"]["statusText"] == "已支付"


def test_cancel_order_then_pay(api, user_header):
    """取消订单后再次支付"""

    add_cart_response = api.add_cart(102, 1, user_header)
    assert add_cart_response.status_code == 200
    assert add_cart_response.json()["items"][0]["productId"] == 102

    create_orders_response = api.create_order(user_header)
    assert create_orders_response.status_code == 200
    orderId = create_orders_response.json()["order"]["id"]
    assert create_orders_response.json()["order"]["statusText"] == "待支付"

    cancel_order_response = api.cancel_order(orderId, user_header)
    assert cancel_order_response.status_code == 200
    assert cancel_order_response.json()["order"]["statusText"] == "已取消"

    pay_orders_response = api.pay_order(orderId, user_header)
    assert pay_orders_response.status_code == 409
    assert pay_orders_response.json()["message"] == "已取消订单不能支付"


def test_pay_order_then_cancel(api, user_header):
    """支付订单后再次取消"""

    add_cart_response = api.add_cart(102, 1, user_header)
    assert add_cart_response.status_code == 200
    assert add_cart_response.json()["items"][0]["productId"] == 102

    create_orders_response = api.create_order(user_header)
    assert create_orders_response.status_code == 200
    orderId = create_orders_response.json()["order"]["id"]
    assert create_orders_response.json()["order"]["statusText"] == "待支付"

    pay_orders_response = api.pay_order(orderId, user_header)
    assert pay_orders_response.status_code == 200
    assert pay_orders_response.json()["order"]["statusText"] == "已支付"

    cancel_order_response = api.cancel_order(orderId, user_header)
    assert cancel_order_response.status_code == 409
    assert cancel_order_response.json()["message"] == "已支付订单不能取消，请走退款流程"


def test_query_nonexistent_order(api, user_header):
    """查询不存在的订单"""

    check_order_response = api.check_detail_order("NO99999", user_header)
    assert check_order_response.status_code == 404
    assert check_order_response.json()["message"] == "订单不存在"


def test_normal_user_reset(api, user_header):
    """普通用户无权重置数据"""

    reset_response = api.post("/reset", headers=user_header)
    assert reset_response.status_code == 403
    assert reset_response.json()["message"] == "只有管理员可以重置练习数据"


def test_admin_reset(api, admin_header):
    """管理员重置数据"""

    reset_response = api.post("/reset", headers=admin_header)
    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "练习数据已重置"