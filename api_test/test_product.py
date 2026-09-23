
def test_get_product_list(api, user_header):
    """登录后获取商品列表"""
    response = api.product_list(user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert len(response.json()["products"]) > 0, "商品列表为空"


def test_get_product_list_without_login(api):
    """未登录获取商品列表"""
    response = api.product_list()
    assert response.status_code == 401
    assert response.json()["message"] == "请先登录，或检查 token 是否正确"


def test_check_product_data(api, user_header):
    """商品列表数据校验"""
    response = api.product_list(user_header)
    assert response.status_code == 200
    assert response.json()["code"] == 0

    products = response.json()["products"]
    assert len(products) > 0

    expected_fields = {"id", "name", "price", "stock"}
    for product in products:
        missing_field = expected_fields - set(product.keys())
        assert not missing_field, f"商品{product.get('id')}缺少{missing_field}字段"

        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str) and product["name"] !=""
        assert isinstance(product["price"], (int, float)) and product["price"] > 0
        assert isinstance(product["stock"], int) and product["stock"] >= 0