import pytest

"""============     创建订单         ==============="""


def test_create_order_with_cart(api, user_header):
    """购物车有商品时创建订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)

    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["order"]["statusText"] == "待支付"


def test_create_order_with_empty_cart(api, user_header):
    """购物车为空时创建订单"""
    response = api.create_order(user_header)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "购物车为空，不能创建订单"


def test_create_order_with_cart_check_cart_empty(api, user_header):
    """检查创建订单后购物车是否清空"""
    api.add_cart(101, 1, user_header)
    api.create_order(user_header)

    response = api.check_cart(user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert len(response.json()["items"]) == 0


def test_check_stock(api, user_header):
    """检查商品库存是否扣减"""
    api.add_cart(101, 1, user_header)
    response = api.product_list(user_header)
    before_stock = response.json()["products"][0]["stock"]

    api.create_order(user_header)
    response = api.product_list(user_header)
    after_stock = response.json()["products"][0]["stock"]
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert after_stock == before_stock - 1


def test_check_order_amount(api, user_header):
    """检查订单金额是否等于商品小计之和"""
    api.add_cart(101, 1, user_header)
    api.add_cart(102, 1, user_header)

    response = api.create_order(user_header)

    items = response.json()["order"]["items"]
    for item in items:
        assert item["price"] * item["quantity"] == item["subtotal"]

    expected_total = sum(item["price"] * item["quantity"] for item in items)
    assert response.json()["order"]["totalAmount"] == expected_total


def test_create_order_without_login(api):
    """未登录创建订单"""
    response = api.create_order()
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     查询订单列表         ==============="""


def test_check_order_list(api, user_header):
    """查询当前用户订单"""
    api.add_cart(101, 1, user_header)
    api.create_order(user_header)

    response = api.check_all_order(user_header)

    orders = response.json()["orders"]

    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert len(orders) > 0


def test_check_order_list_new_order_first(api, user_header):
    """新订单是否排在前面"""
    api.add_cart(101, 1, user_header)
    api.create_order(user_header)

    api.add_cart(102, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    orders = api.check_all_order(user_header).json()["orders"]
    assert len(orders) >= 2
    assert orders[0]["id"] == orderid


def test_check_order_status_text(api, user_header):
    """订单状态文案是否正确"""
    api.add_cart(101, 1, user_header)
    api.create_order(user_header)

    response = api.check_all_order(user_header)

    orders = response.json()["orders"]

    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert orders[0]["statusText"] == "待支付"


def test_check_order_list_without_login(api):
    """未登录查询用户订单"""
    response = api.check_all_order()
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     查询订单详情         ==============="""


def test_check_order_detail(api, user_header):
    """查询存在订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    response = api.check_detail_order(orderid, user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["order"]["id"] == orderid


def test_check_order_detail_nonexistent_order(api, user_header):
    """查询不存在订单"""
    response = api.check_detail_order("99999", user_header)
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert response.json()["message"] == "订单不存在"


def test_check_order_detail_without_login(api, user_header):
    """	未登录查询订单下详情"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    response = api.check_detail_order(orderid)
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     支付订单         ==============="""


def test_pay_order(api, user_header):
    """支付待支付订单"""
    api.add_cart(101, 1, user_header)

    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]
    assert response.json()["order"]["statusText"] == "待支付"

    response = api.pay_order(orderid, user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["order"]["statusText"] == "已支付"


def test_pay_order_cancelled_order(api, user_header):
    """支付已取消订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]
    assert response.json()["order"]["statusText"] == "待支付"

    response = api.cancel_order(orderid, user_header)
    assert response.json()["order"]["statusText"] == "已取消"

    response = api.pay_order(orderid, user_header)
    assert response.status_code == 409
    assert response.json()["code"] == 409
    assert response.json()["message"] == "已取消订单不能支付"


def test_pay_order_nonexistent_order(api, user_header):
    """支付不存在订单"""
    response = api.pay_order("99999", user_header)
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert response.json()["message"] == "订单不存在"


@pytest.mark.xfail(
    reason="已知缺陷：重复支付订单时返回 code=0（对应 test_cases.md pay_orders_004）",
    strict=True
)
def test_pay_order_duplicate(api, user_header):
    """重复支付订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]
    api.pay_order(orderid, user_header)
    response = api.pay_order(orderid, user_header)
    assert response.status_code != 200 or response.json()["code"] != 0


def test_pay_order_without_login(api, user_header):
    """未登录支付订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]
    response = api.pay_order(orderid)
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     取消订单         ==============="""


def test_cancel_order(api, user_header):
    """取消待支付订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    response = api.cancel_order(orderid, user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["order"]["statusText"] == "已取消"


def test_cancel_order_paid_order(api, user_header):
    """取消已支付订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]
    api.pay_order(orderid, user_header)

    response = api.cancel_order(orderid, user_header)
    assert response.status_code == 409
    assert response.json()["code"] == 409
    assert response.json()["message"] == "已支付订单不能取消，请走退款流程"


def test_cancel_order_nonexistent_order(api, user_header):
    """取消不存在订单"""
    api.add_cart(101, 1, user_header)
    api.create_order(user_header)

    response = api.cancel_order("99999", user_header)
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert response.json()["message"] == "订单不存在"


@pytest.mark.xfail(
    reason="已知缺陷：取消已取消订单时返回 code=0（对应 test_cases.md cancel_orders_004）",
    strict=True
)
def test_cancel_order_cancelled_order(api, user_header):
    """取消已取消订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    api.cancel_order(orderid, user_header)
    response = api.cancel_order(orderid, user_header)
    assert response.status_code != 200 or response.json()["code"] != 0


def test_cancel_order_without_login(api, user_header):
    """未登录取消订单"""
    api.add_cart(101, 1, user_header)
    response = api.create_order(user_header)
    orderid = response.json()["order"]["id"]

    response = api.cancel_order(orderid)
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"
