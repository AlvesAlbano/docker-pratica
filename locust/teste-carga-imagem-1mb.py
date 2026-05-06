from locust import HttpUser, task, between


url_imagem_1mb = "/wp-content/uploads/2026/04/img-1mb.jpg"


class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Host": "localhost:8080"
    }

    @task(1)
    def imagem_1mb(self):
        self.client.get(
            url_imagem_1mb,
            name="Imagem 1MB",
            headers=self.headers
        )