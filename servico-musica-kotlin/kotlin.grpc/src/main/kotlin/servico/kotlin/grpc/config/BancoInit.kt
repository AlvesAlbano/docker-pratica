package servico.kotlin.grpc.config

import org.springframework.boot.CommandLineRunner
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import servico.kotlin.grpc.entity.Musica
import servico.kotlin.grpc.entity.Playlist
import servico.kotlin.grpc.entity.Usuario
import servico.kotlin.grpc.repository.MusicaRepository
import servico.kotlin.grpc.repository.PlaylistRepository
import servico.kotlin.grpc.repository.UsuarioRepository

@Configuration
class BancoInit {

    @Bean
    fun commandLineRunner(
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