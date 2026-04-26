from locust import HttpUser, task, between


class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Host": "localhost:8080"
    }

    @task(1)
    def post_texto_400kb(self):
        self.client.get("/?p=12", name="Post texto 400KB", headers=self.headers)

    @task(1)
    def post_imagem_1mb(self):
        self.client.get("/?p=6", name="Post imagem 1MB", headers=self.headers)

    @task(1)
    def post_imagem_300kb(self):
        self.client.get("/?p=9", name="Post imagem 300KB", headers=self.headers)