package servico.java.rest.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import servico.java.rest.entity.Musica;
import servico.java.rest.entity.Playlist;
import servico.java.rest.entity.Usuario;
import servico.java.rest.repository.MusicaRepository;
import servico.java.rest.repository.PlaylistRepository;
import servico.java.rest.repository.UsuarioRepository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/servico-rest-java/playlist")
public class PlaylistController {

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private MusicaRepository musicaRepository;

    @PostMapping("/usuario/{idUsuario}")
    public List<Playlist> playlistUsuario(@PathVariable long idUsuario){

        Optional<Usuario> usuario = usuarioRepository.findById(idUsuario);

        if (usuario.isEmpty()){
            return Collections.emptyList();
        }

        return usuario.get().getPlaylistsUsuario();
    }

    @PostMapping("/musica/{idMusica}")
    public List<Playlist> musicasEspecifica(@PathVariable long idMusica){

        return playlistRepository.findByMusicasId(idMusica);
    }


}