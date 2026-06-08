from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def executar_get(self, path, nome):
        with self.client.get(path, catch_response=True, name=nome) as response:
            if response.status_code != 200:
                response.failure(f"Status inesperado: {response.status_code}")

    def executar_post(self, path, nome):
        with self.client.post(path, catch_response=True, name=nome) as response:
            if response.status_code not in [200, 201]:
                response.failure(f"Status inesperado: {response.status_code}")

    @task
    def listar_usuarios(self):
        self.executar_get(
            "/servico-rest-kotlin/usuario/todos-usuarios",
            "todos-usuarios"
        )

    @task
    def listar_musicas(self):
        self.executar_get(
            "/servico-rest-kotlin/musica/todas-musicas",
            "todas-musicas"
        )

    @task
    def playlist_usuario(self):
        self.executar_post(
            "/servico-rest-kotlin/playlist/usuario/4",
            "playlist-usuario"
        )

    @task
    def playlist_musica(self):
        self.executar_post(
            "/servico-rest-kotlin/playlist/musica/4",
            "playlist-musica"
        )