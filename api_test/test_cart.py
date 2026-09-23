import pytest

"""============     查询购物车         ==============="""


def test_check_cart(api, user_header):
    """正常查询购物车"""
    response = api.check_cart(user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert "items" in response.json()
    assert "totalAmount" in response.json()


def test_check_cart_data(api, user_header):
    """购物车商品数据校验"""
    api.add_cart(102, 1, user_header)
    response = api.check_cart(user_header)

    items = response.json()["items"]
    assert len(items) > 0, "购物车为空"

    for item in items:
        assert item["productId"] == 102
        assert item["price"] > 0
        assert item["quantity"] == 1
        assert isinstance(item["name"], str) and item["name"] !=""

    expected_total = sum(item["price"] * item["quantity"] for item in items)
    assert response.json()["totalAmount"] == expected_total


def test_check_cart_without_login(api):
    """未登录查询购物车"""
    response = api.check_cart()
    assert response.status_code == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     加入购物车         ==============="""


def test_add_cart(api, user_header):
    """正常加入购物车"""
    add_cart_response = api.add_cart(101, 1, user_header)
    assert add_cart_response.status_code == 200
    assert add_cart_response.json()["code"] == 0
    assert add_cart_response.json()["items"][0]["productId"] == 101


def test_add_cart_duplicate(api, user_header):
    """重复加入同一商品"""
    api.add_cart(101, 1, user_header)
    add_cart_response = api.add_cart(101, 1, user_header)
    assert add_cart_response.status_code == 200
    assert add_cart_response.json()["code"] == 0
    assert add_cart_response.json()["items"][0]["quantity"] == 2


@pytest.mark.xfail(
    reason="已知缺陷：quantity=0 时仍返回 code=0 并累加数量（对应 test_cases.md add_cart_003）",
    strict=True
)
def test_add_cart_quantity_zero(api, user_header):
    response = api.add_cart(101, 0, user_header)
    assert response.status_code != 200 or response.json()["code"] != 0


def test_add_cart_quantity_negative(api, user_header):
    """quantity为负数"""
    response = api.add_cart(101, -1, user_header)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "商品数量必须大于 0"


@pytest.mark.xfail(
    reason="已知缺陷：quantity过大时仍返回 code=0（对应 test_cases.md add_cart_005）",
    strict=True
)
def test_add_cart_quantity_too_large(api, user_header):
    """quantity过大"""
    response = api.add_cart(101, 999, user_header)
    assert response.status_code != 200 or response.json()["code"] != 0


def test_add_cart_nonexistent_product_id(api, user_header):
    """不存在的productId"""
    response = api.add_cart(0, 1, user_header)
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert response.json()["message"] == "商品不存在"


def test_add_cart_out_of_stock(api, user_header):
    """库存为0的商品"""
    response = api.add_cart(104, 1, user_header)
    assert response.status_code == 409
    assert response.json()["code"] == 409
    assert response.json()["message"] == "商品库存不足"


def test_add_cart_without_login(api):
    """未登录加入购物车"""
    response = api.add_cart(101, 1)
    assert response.status_code == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


"""============     删除购物车         ==============="""


def test_delete_cart_exist_product_id(api, user_header):
    """删除存在商品"""
    api.add_cart(101, 1, user_header)
    response = api.delete_cart(101, user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0


@pytest.mark.xfail(
    reason="已知缺陷：删除不存在的商品时返回 code=0, 并返回购物车列表（对应 test_cases.md delete_cart_002）",
    strict=True
)
def test_delete_cart_nonexistent_product_id(api, user_header):
    """删除不存在商品"""
    response = api.delete_cart(9999, user_header)
    assert response.status_code != 200 or response.json()["code"] != 0


def test_delete_cart_with_check_data(api, user_header):
    """检查购物车数据是否更新：商品消失、总金额正确更新"""
    api.add_cart(101, 1, user_header)
    api.add_cart(102, 2, user_header)
    api.delete_cart(101, user_header)

    response = api.check_cart(user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0

    items = response.json()["items"]
    ids = [i["productId"] for i in items]
    assert 101 not in ids, "删除后商品101仍在购物车中"
    assert 102 in ids, "删除操作误伤了其他商品"

    expected_total = sum(item["price"] * item["quantity"] for item in items)
    assert response.json()["totalAmount"] == pytest.approx(expected_total), "总金额未正确更新"


def test_delete_cart_without_login(api):
    """未登录删除商品"""
    response = api.delete_cart(102)
    assert response.status_code == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"