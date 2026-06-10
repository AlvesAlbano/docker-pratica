package servico.kotlin.rest.config

import org.springframework.boot.CommandLineRunner
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import servico.kotlin.rest.entity.Musica
import servico.kotlin.rest.entity.Playlist
import servico.kotlin.rest.entity.Usuario
import servico.kotlin.rest.repository.MusicaRepository
import servico.kotlin.rest.repository.PlaylistRepository
import servico.kotlin.rest.repository.UsuarioRepository

@Configuration
open class BancoInit {

    @Bean
    open fun commandLineRunner(
        musicaRepository: MusicaRepository,
        playlistRepository: PlaylistRepository,
        usuarioRepository: UsuarioRepository
    ): CommandLineRunner {

        val QTD_MUSICAS = 1000
        val QTD_USUARIOS = 1000
        val QTD_MUSICAS_PLAYLIST = 4

        return CommandLineRunner {

            for (i in 0..QTD_MUSICAS) {
                musicaRepository.save(
                    Musica(
                        "Musica $i",
                        "Artista $i"
                    )
                )
            }

            val min: Short = 16
            val max: Short = 45

            for (i in 0..QTD_USUARIOS) {
                val idade = (min + (Math.random() * ((max - min) + 1)).toInt()).toShort()

                usuarioRepository.save(
                    Usuario(
                        "Usuario $i",
                        idade
                    )
                )
            }

            val musicas = musicaRepository.findAll().toMutableList()

            for (usuario in usuarioRepository.findAll()) {

                val playlist = Playlist("playlist do usuario de id ${usuario.id}")
                playlist.usuario = usuario

                musicas.shuffle()

                playlist.musicas.addAll(musicas.take(QTD_MUSICAS_PLAYLIST))

                playlistRepository.save(playlist)
            }
        }
    }
}