package servico.kotlin.soap.controller

import jakarta.transaction.Transactional
import org.springframework.ws.server.endpoint.annotation.Endpoint
import org.springframework.ws.server.endpoint.annotation.PayloadRoot
import org.springframework.ws.server.endpoint.annotation.RequestPayload
import org.springframework.ws.server.endpoint.annotation.ResponsePayload
import servico.kotlin.soap.generated.*
import servico.kotlin.soap.repository.PlaylistRepository
import servico.kotlin.soap.repository.UsuarioRepository

@Endpoint
class PlaylistController(
    private val usuarioRepository: UsuarioRepository,
    private val playlistRepository: PlaylistRepository
) {

    @Transactional
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getPlaylistsByUsuarioRequest")
    @ResponsePayload
    fun getByUsuario(
        @RequestPayload request: GetPlaylistsByUsuarioRequest
    ): GetPlaylistsByUsuarioResponse {

        val response = GetPlaylistsByUsuarioResponse()

        val usuario = usuarioRepository.findById(request.idUsuario).orElse(null)
            ?: return response

        usuario.playlistsUsuario.forEach { p ->
            val playlist = Playlist().apply {
                id = p.id!!
                nome = p.nome
            }
            response.playlist.add(playlist)
        }

        return response
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getPlaylistsByMusicaRequest")
    @ResponsePayload
    fun getByMusica(
        @RequestPayload request: GetPlaylistsByMusicaRequest
    ): GetPlaylistsByMusicaResponse {

        val response = GetPlaylistsByMusicaResponse()

        playlistRepository.findByMusicasId(request.idMusica)
            ?.forEach { p ->
                val playlist = Playlist().apply {
                    id = p?.id!!
                    nome = p.nome
                }
                response.playlist.add(playlist)
            }

        return response
    }

    companion object {
        private const val NAMESPACE_URI = "http://soap.kotlin.servico/playlist"
    }
}