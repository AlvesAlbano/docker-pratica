package servico.kotlin.rest.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import servico.kotlin.rest.entity.Musica;
import servico.kotlin.rest.entity.Playlist;
import servico.kotlin.rest.entity.Usuario;
import servico.kotlin.rest.repository.MusicaRepository;
import servico.kotlin.rest.repository.PlaylistRepository;
import servico.kotlin.rest.repository.UsuarioRepository;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Configuration
public class BancoInit {

    @Bean
    CommandLineRunner commandLineRunner(MusicaRepository musicaRepository, PlaylistRepository playlistRepository, UsuarioRepository usuarioRepository) {

        return args -> {
            // popular musica repo
            for (int i = 0; i < 200; i++) {
                musicaRepository.<Musica>save(
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

            for (int i = 0; i < 200; i++) {
                idade = (short) (min + (int)(Math.random() * ((max - min) + 1)));
                usuarioRepository.<Usuario>save(
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
                        String.format("playlist do usuario de id %d", usuario.id)
                );

                playlist.usuario = usuario;

//                for (Musica musica : musicas) {
//                    playlist.getMusicas().add(musica);
//                }

                List<Musica> copia = new ArrayList<>(musicas);
                Collections.shuffle(copia);

                playlist.musicas.addAll(copia.subList(0, 3));

                playlistRepository.<Playlist>save(playlist);
            }
        };
    }
}
