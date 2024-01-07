from locust import HttpUser, task, between

class MyLoadTestUser(HttpUser):
    wait_time = between(1, 5)  # wait time between requests

    @task
    def product_check(self):
        self.client.get('http://127.0.0.1:8000/product-detail/21')

    @task
    def home_page(self):
        self.client.get('http://127.0.0.1:8000/')

    @task
    def checkout(self):
        self.client.get('http://127.0.0.1:8000/checkout/')


