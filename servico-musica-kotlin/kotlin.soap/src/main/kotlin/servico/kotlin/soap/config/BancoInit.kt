package servico.kotlin.soap.config

import org.springframework.boot.CommandLineRunner
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import servico.kotlin.soap.entity.Musica
import servico.kotlin.soap.entity.Playlist
import servico.kotlin.soap.entity.Usuario
import servico.kotlin.soap.repository.MusicaRepository
import servico.kotlin.soap.repository.PlaylistRepository
import servico.kotlin.soap.repository.UsuarioRepository

@Configuration
class BancoInit {

    @Bean
    fun commandLineRunner(
        musicaRepository: MusicaRepository,
        playlistRepository: PlaylistRepository,
        usuarioRepository: UsuarioRepository
    ): CommandLineRunner {

        val tamanhoBd = 199
        return CommandLineRunner {

            // músicas
            for (i in 0..tamanhoBd) {
                musicaRepository.save(
                    Musica(
                        "Musica $i",
                        "Artista $i"
                    )
                )
            }

            // usuários
            val min = 16
            val max = 45

            for (i in 0..tamanhoBd) {
                val idade = (min..max).random().toShort()

                usuarioRepository.save(
                    Usuario(
                        "Usuario $i",
                        idade
                    )
                )
            }

            // playlists
            val musicas = musicaRepository.findAll()

            for (usuario in usuarioRepository.findAll()) {

                val playlist = Playlist(
                    "playlist do usuario de id ${usuario.id}"
                )

                playlist.usuario = usuario

                val copia = musicas.toMutableList()
                copia.shuffle()

                playlist.musicas.addAll(copia.take(3))

                playlistRepository.save(playlist)
            }
        }
    }
}