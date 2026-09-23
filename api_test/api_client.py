import requests


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, path, headers=None, json=None):
        return requests.post(
            f"{self.base_url}{path}",
            headers=headers,
            json=json
        )

    def get(self, path, headers=None):
        return requests.get(
            f"{self.base_url}{path}",
            headers=headers
        )

    def login_post(self, username, password):
        return self.post(
            "/login",
            json={
                "username": username,
                "password": password
            }
        )

    def login_without_password(self, username):
        return self.post(
            "/login",
            json={
                "username": username
            }
        )

    def product_list(self, header=None):
        return self.get(
            "/products",
            headers=header
        )

    def check_cart(self, header=None):
        return self.get(
            "/cart",
            headers=header
        )

    def add_cart(self, product_id, quantity, header=None):
        return self.post(
            "/cart",
            headers=header,
            json={
                "productId": product_id,
                "quantity": quantity
            }
        )

    def create_order(self, header=None):
        return self.post(
            "/orders",
            headers=header
        )

    def pay_order(self, order_id, header=None):
        return self.post(
            f"/orders/{order_id}/pay",
            headers=header
        )

    def cancel_order(self, order_id, header=None):
        return self.post(
            f"/orders/{order_id}/cancel",
            headers=header
        )

    def check_all_order(self, header=None):
        return self.get(
            "/orders",
            headers=header
        )

    def check_detail_order(self, order_id, header=None):
        return self.get(
            f"/orders/{order_id}",
            headers=header
        )

    def delete_cart(self, product_id, header=None):
        return requests.delete(
            f"{self.base_url}/cart/{product_id}",
            headers=header
        )