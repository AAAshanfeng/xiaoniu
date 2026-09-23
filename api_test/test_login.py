import pytest


def test_login_success(api):
    """正确账号密码，应该登录成功，返回200"""
    response = api.login_post("tester", "123456")
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert "token" in response.json()


@pytest.mark.parametrize(
    "username, password",
    [
        ("tester", "wrong_password"),   # 密码错误
        ("wrong_username", "123456"),   # 用户名错误
        ("tester", ""),                 # 密码为空
        ("", "123456"),                 # 用户名为空
        ("tester", None),               # 密码字段为空
        (123456, "123456"),             # 用户名类型错误
        ("tester", 123456)              # 密码类型错误
    ],
    ids=[
        "wrong_password",
        "wrong_username",
        "password_empty",
        "username_empty",
        "password_field_empty",
        "username_type_error",
        "password_type_error"
    ]
)
def test_login_wrong_password(api, username, password):
    if password is None:
        response = api.login_without_password(username)
    else:
        response = api.login_post(username, password)

    assert response.status_code == 401
    assert "账号或密码错误" in response.json()["message"]