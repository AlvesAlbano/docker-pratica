from locust import HttpUser, task, between


# url_postagem_imagem_1mb = "/?p=7"
# url_postagem_imagem_300kb = "/?p=9" 
# url_postagem_texto_400kb = "/?p=5"
 
url_postagem_imagem_1mb = "/?p=6"
url_postagem_imagem_300kb = "/?p=9"
url_postagem_texto_400kb = "/?p=12"

class SiteWordPress(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Host": "localhost:8080"
    }
    
    @task(1)
    def post_texto_400kb(self):
        self.client.get(url_postagem_texto_400kb, name="Post texto 400KB", headers=self.headers)

    # @task(1)
    # def post_imagem_1mb(self):
    #     self.client.get(url_postagem_imagem_1mb, name="Post imagem 1MB", headers=self.headers)

    # @task(1)
    # def post_imagem_300kb(self):
    #     self.client.get(url_postagem_imagem_300kb, name="Post imagem 300KB", headers=self.headers)