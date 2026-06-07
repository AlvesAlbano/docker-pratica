package servico.kotlin.soap.controller

import org.springframework.ws.server.endpoint.annotation.Endpoint
import org.springframework.ws.server.endpoint.annotation.PayloadRoot
import org.springframework.ws.server.endpoint.annotation.RequestPayload
import org.springframework.ws.server.endpoint.annotation.ResponsePayload
import servico.kotlin.soap.generated.GetTodasMusicasRequest
import servico.kotlin.soap.generated.GetTodasMusicasResponse
import servico.kotlin.soap.generated.Musica
import servico.kotlin.soap.repository.MusicaRepository

@Endpoint
class MusicaController(private val musicaRepository: MusicaRepository) {

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getTodasMusicasRequest")
    @ResponsePayload
    fun getTodasMusicas(
        @RequestPayload request: GetTodasMusicasRequest?
    ): GetTodasMusicasResponse {
        val response: GetTodasMusicasResponse =
            GetTodasMusicasResponse()

        musicaRepository.findAll().forEach { m ->
            val soapMusica = Musica()
            soapMusica.id = m.id!!
            soapMusica.nome = m.nome
            soapMusica.artista = m.artista

            response.musica.add(soapMusica)
        }

        return response
    }

    companion object {
        private const val NAMESPACE_URI = "http://soap.kotlin.servico/musica"
    }
}