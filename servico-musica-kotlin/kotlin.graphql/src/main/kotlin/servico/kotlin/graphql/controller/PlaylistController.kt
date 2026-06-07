package servico.kotlin.graphql.controller

import org.springframework.graphql.data.method.annotation.Argument
import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller
import servico.kotlin.graphql.entity.Playlist
import servico.kotlin.graphql.repository.PlaylistRepository
import servico.kotlin.graphql.repository.UsuarioRepository

@Controller
class PlaylistController(
    private val playlistRepository: PlaylistRepository,
    private val usuarioRepository: UsuarioRepository
) {
    @QueryMapping
    fun playlistsDoUsuario(@Argument idUsuario: Long): MutableList<Playlist?>? {
        val usuario = usuarioRepository.findById(idUsuario)

        if (usuario.isEmpty()) {
            return mutableListOf<Playlist?>()
        }

        return usuario.get().playlistsUsuario
    }

    @QueryMapping
    fun playlistsPorMusica(@Argument idMusica: Long?): MutableList<Playlist?>? {
        return playlistRepository.findByMusicasId(idMusica)
    }
}