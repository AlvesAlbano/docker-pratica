from locust import HttpUser, task, between

soap_body_todas_musicas = """
<soapenv:Envelope
 xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:mus="http://soap.kotlin.servico/musica">

   <soapenv:Body>
      <mus:getTodasMusicasRequest/>
   </soapenv:Body>

</soapenv:Envelope>
"""

soap_body_todos_usuarios = """
<soapenv:Envelope
 xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:usr="http://soap.kotlin.servico/usuario">

   <soapenv:Body>
      <usr:getTodosUsuariosRequest/>
   </soapenv:Body>

</soapenv:Envelope>
"""

soap_body_usuario_id = """
<soapenv:Envelope
 xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:pl="http://soap.kotlin.servico/playlist">

   <soapenv:Body>
      <pl:getPlaylistsByUsuarioRequest>
         <pl:idUsuario>8</pl:idUsuario>
      </pl:getPlaylistsByUsuarioRequest>
   </soapenv:Body>

</soapenv:Envelope>
"""

soap_body_playlist_id = """
<soapenv:Envelope
 xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:pl="http://soap.kotlin.servico/playlist">

   <soapenv:Body>
      <pl:getPlaylistsByMusicaRequest>
         <pl:idMusica>1</pl:idMusica>
      </pl:getPlaylistsByMusicaRequest>
   </soapenv:Body>

</soapenv:Envelope>
"""

class SoapUser(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Content-Type": "text/xml;charset=UTF-8"
    }

    def executar_soap(self, body, nome):
        with self.client.post(
            "/ws",
            data=body,
            headers=self.headers,
            name=nome,
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"HTTP {response.status_code}: {response.text[:300]}"
                )

            elif "Fault" in response.text:
                response.failure(
                    f"SOAP Fault: {response.text[:300]}"
                )

            else:
                response.success()

    @task
    def todas_musicas(self):
        self.executar_soap(
            soap_body_todas_musicas,
            "SOAP_getTodasMusicas"
        )

    @task
    def todos_usuarios(self):
        self.executar_soap(
            soap_body_todos_usuarios,
            "SOAP_getTodosUsuarios"
        )

    @task
    def playlists_por_usuario(self):
        self.executar_soap(
            soap_body_usuario_id,
            "SOAP_getPlaylistsByUsuario"
        )

    @task
    def playlists_por_musica(self):
        self.executar_soap(
            soap_body_playlist_id,
            "SOAP_getPlaylistsByMusica"
        )