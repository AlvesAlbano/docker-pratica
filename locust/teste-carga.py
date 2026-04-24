from locust import HttpUser, task, between


class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def post_imagem_1mb(self):
        self.client.get("/?p=14", name="Post imagem 1MB")

    @task(1)
    def post_imagem_300kb(self):
        self.client.get("/?p=11", name="Post imagem 300KB")

    @task(1)
    def post_texto_400kb(self):
        self.client.get("/?p=8", name="Post texto 400KB")