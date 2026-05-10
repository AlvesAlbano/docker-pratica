from locust import HttpUser, task, between


url_imagem_300kb = "/wp-content/uploads/2026/04/img-300kb.jpg"


class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Host": "localhost:8080"
    }

    @task(1)
    def imagem_300kb(self):
        self.client.get(
            url_imagem_300kb,
            name="Imagem 300KB",
            headers=self.headers
        )