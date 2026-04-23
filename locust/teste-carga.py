from locust import HttpUser, task, between

class Site(HttpUser):
# docker restart nginx
    host = "http://localhost:8080"
    wait_time = between(1, 3)

    @task
    def post_imagem_1mb(self):
        self.client.get(
            "/?p=14"
        )

    @task
    def post_imagem_300kb(self):
        self.client.get(
            "/?p=11"
        )

    @task
    def post_texto_400kb(self):
        self.client.get(
            "/?p=8"
        )
    