from locust import HttpUser, task, between
import random

class GraphQLUser(HttpUser):
    wait_time = between(1, 3)

    def graphql_request(self, query, variables=None, name="GraphQL"):
        with self.client.post(
            "/graphql",
            json={
                "query": query,
                "variables": variables or {}
            },
            name=name,
            catch_response=True
        ) as response:

            try:
                data = response.json()

                if "errors" in data:
                    response.failure(f"GraphQL Error: {data['errors']}")
                else:
                    response.success()

            except Exception as e:
                response.failure(f"Resposta inválida: {e}")

    @task
    def todos_usuarios(self):
        query = """
        query {
          todosUsuarios {
            playlistsUsuario {
              musicas {
                nome
                id
                artista
              }
              nome
              id
            }
            nome
            idade
            id
          }
        }
        """

        self.graphql_request(
            query=query,
            name="todosUsuarios"
        )

    @task
    def playlists_do_usuario(self):
        query = """
        query {
          playlistsDoUsuario(idUsuario: "8") {
            id
            musicas {
              nome
              id
              artista
            }
            nome
          }
        }
        """

        self.graphql_request(
            query=query,
            name="playlistsDoUsuario"
        )

    @task(2)
    def playlists_por_musica(self):
        query = """
        query MyQuery($idMusica: ID!) {
          playlistsPorMusica(idMusica: $idMusica) {
            id
            nome
            musicas {
              nome
              id
              artista
            }
          }
        }
        """

        variables = {
            "idMusica": str(random.randint(1, 20))
        }

        self.graphql_request(
            query=query,
            variables=variables,
            name="playlistsPorMusica"
        )

    @task
    def todas_as_musicas(self):
        query = """
        query {
          todasAsMusicas {
            artista
            id
            nome
          }
        }
        """

        self.graphql_request(
            query=query,
            name="todasAsMusicas"
        )