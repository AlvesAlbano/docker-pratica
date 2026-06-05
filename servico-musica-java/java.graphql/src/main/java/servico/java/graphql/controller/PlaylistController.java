package servico.java.graphql.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import servico.java.graphql.entity.Playlist;
import servico.java.graphql.entity.Usuario;
import servico.java.graphql.repository.PlaylistRepository;
import servico.java.graphql.repository.UsuarioRepository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Controller
public class PlaylistController {

    private final PlaylistRepository playlistRepository;

    private final UsuarioRepository usuarioRepository;

    public PlaylistController(PlaylistRepository playlistRepository, UsuarioRepository usuarioRepository) {
        this.playlistRepository = playlistRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @QueryMapping
    public List<Playlist> playlistsDoUsuario(@Argument Long idUsuario) {

        Optional<Usuario> usuario = usuarioRepository.findById(idUsuario);

        if (usuario.isEmpty()) {
            return Collections.emptyList();
        }

        return usuario.get().getPlaylistsUsuario();
    }

    @QueryMapping
    public List<Playlist> playlistsPorMusica(@Argument Long idMusica) {
        return playlistRepository.findByMusicasId(idMusica);
    }
}