package servico.java.soap.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import servico.java.soap.entity.Musica;
import servico.java.soap.entity.Playlist;
import servico.java.soap.entity.Usuario;
import servico.java.soap.repository.MusicaRepository;
import servico.java.soap.repository.PlaylistRepository;
import servico.java.soap.repository.UsuarioRepository;

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

            for (int i = 0; i < 200; i++) {
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

                playlist.getMusicas().addAll(copia.subList(0, 3));

                playlistRepository.save(playlist);
            }
        };
    }
}
