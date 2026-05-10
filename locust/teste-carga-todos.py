from locust import HttpUser, task, between


url_imagem_1mb = "/wp-content/uploads/2026/04/img-1mb.jpg"
url_imagem_300kb = "/wp-content/uploads/2026/04/img-300kb.jpg"
url_postagem_texto_400kb = "/?p=12"


class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Host": "localhost:8080"
    }

    @task(1)
    def post_texto_400kb(self):
        self.client.get(
            url_postagem_texto_400kb,
            name="Post texto 400KB",
            headers=self.headers
        )

    @task(1)
    def imagem_1mb(self):
        self.client.get(
            url_imagem_1mb,
            name="Imagem 1MB",
            headers=self.headers
        )

    @task(1)
    def imagem_300kb(self):
        self.client.get(
            url_imagem_300kb,
            name="Imagem 300KB",
            headers=self.headers
        )