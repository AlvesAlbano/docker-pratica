package servico.java.grpc.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import servico.java.grpc.entity.Musica;
import servico.java.grpc.entity.Playlist;
import servico.java.grpc.entity.Usuario;
import servico.java.grpc.repository.MusicaRepository;
import servico.java.grpc.repository.PlaylistRepository;
import servico.java.grpc.repository.UsuarioRepository;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Configuration
public class BancoInit {

    @Bean
    CommandLineRunner commandLineRunner(MusicaRepository musicaRepository, PlaylistRepository playlistRepository, UsuarioRepository usuarioRepository) {

        final int QTD_MUSICAS = 1000;
        final int QTD_USUARIOS = 1000;
        final int QTD_MUSICAS_PLAYLIST = 4;

        return args -> {
            // popular musica repo
            for (int i = 0; i < QTD_MUSICAS; i++) {
                musicaRepository.save(
                        new Musica(
                                String.format("Musica %d",i),
                                String.format("Artista %d",i)
                        )
                );
            }

            // popular usuario repo
            int min = 16;
            int max = 45;
            short idade;

            for (int i = 0; i < QTD_USUARIOS; i++) {
                idade = (short) (min + (int)(Math.random() * ((max - min) + 1)));
                usuarioRepository.save(
                        new Usuario(
                                String.format("Usuario %d",i),
                                idade
                        )
                );
            }

            // popular playlist usuario
            List<Musica> musicas = musicaRepository.findAll();

            for (Usuario usuario : usuarioRepository.findAll()) {

                Playlist playlist = new Playlist(
                        String.format("playlist do usuario de id %d", usuario.getId())
                );

                playlist.setUsuario(usuario);

//                for (Musica musica : musicas) {
//                    playlist.getMusicas().add(musica);
//                }

                List<Musica> copia = new ArrayList<>(musicas);
                Collections.shuffle(copia);

                playlist.getMusicas().addAll(copia.subList(0, QTD_MUSICAS_PLAYLIST));

                playlistRepository.save(playlist);
            }
        };
    }
}