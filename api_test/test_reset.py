
def test_normal_user_reset(api, user_header):
    """普通用户重置练习数据"""
    response = api.post("/reset", headers=user_header)

    assert response.status_code == 403
    assert response.json()["message"] == "只有管理员可以重置练习数据"


def test_admin_reset(api, admin_header):
    """管理员重置练习数据"""
    response = api.post("/reset", headers=admin_header)

    assert response.status_code == 200
    assert response .json()["code"] == 0
    assert response.json()["message"] == "练习数据已重置"


def test_reset_data_recovery(api, admin_header):
    """重置后订单、购物车、库存恢复"""
    product_list_response = api.product_list(admin_header)
    products = product_list_response.json()["products"]
    before_stock = {product["id"]: product["stock"] for product in products}

    cart_response = api.check_cart(admin_header)
    items = cart_response.json()["items"]
    before_cart = [(i["productId"], i["quantity"]) for i in items]

    order_response = api.check_all_order(admin_header)
    orders = order_response.json()["orders"]
    before_order = {o["id"] for o in orders}

    r1 = api.add_cart(101, 2, admin_header)
    assert r1.json()["code"] == 0
    r2 = api.create_order(admin_header)
    assert r2.json()["code"] == 0

    response = api.post("/reset", headers=admin_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["message"] == "练习数据已重置"

    product_list_response = api.product_list(admin_header)
    products = product_list_response.json()["products"]
    after_stock = {product["id"]: product["stock"] for product in products}

    cart_response = api.check_cart(admin_header)
    items = cart_response.json()["items"]
    after_cart = [(i["productId"], i["quantity"]) for i in items]

    order_response = api.check_all_order(admin_header)
    orders = order_response.json()["orders"]
    after_order = {o["id"] for o in orders}

    assert before_stock == after_stock
    assert before_cart == after_cart
    assert before_order == after_order