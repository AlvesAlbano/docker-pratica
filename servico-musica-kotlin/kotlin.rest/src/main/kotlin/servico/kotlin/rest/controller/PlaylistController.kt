package servico.kotlin.rest.controller

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import servico.kotlin.rest.entity.Playlist
import servico.kotlin.rest.repository.MusicaRepository
import servico.kotlin.rest.repository.PlaylistRepository
import servico.kotlin.rest.repository.UsuarioRepository

@RestController
@RequestMapping("/servico-rest-kotlin/playlist")
class PlaylistController {
    @Autowired
    private val playlistRepository: PlaylistRepository? = null

    @Autowired
    private val usuarioRepository: UsuarioRepository? = null

    @Autowired
    private val musicaRepository: MusicaRepository? = null

    @PostMapping("/usuario/{idUsuario}")
    fun playlistUsuario(@PathVariable idUsuario: Long): MutableList<Playlist?> {
        val usuario = usuarioRepository!!.findById(idUsuario)

        if (usuario.isEmpty()) {
            return mutableListOf<Playlist?>()
        }

        return usuario.get().playlistsUsuario
    }

    @PostMapping("/musica/{idMusica}")
    fun musicasEspecifica(@PathVariable idMusica: Long): MutableList<Playlist?>? {
        return playlistRepository!!.findByMusicasId(idMusica)
    }
}