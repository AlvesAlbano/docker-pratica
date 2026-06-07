package servico.java.soap.controller;

import jakarta.transaction.Transactional;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import servico.java.soap.entity.Usuario;
import servico.java.soap.generated.*;
import servico.java.soap.repository.PlaylistRepository;
import servico.java.soap.repository.UsuarioRepository;

@Endpoint
public class PlaylistController {

    private static final String NAMESPACE_URI = "http://soap.java.servico/playlist";

    private final UsuarioRepository usuarioRepository;
    private final PlaylistRepository playlistRepository;

    public PlaylistController(UsuarioRepository usuarioRepository, PlaylistRepository playlistRepository) {
        this.usuarioRepository = usuarioRepository;
        this.playlistRepository = playlistRepository;
    }

    // =========================
    // PLAYLIST POR USUÁRIO
    // =========================
    @Transactional
    @PayloadRoot(
            namespace = NAMESPACE_URI,
            localPart = "getPlaylistsByUsuarioRequest"
    )
    @ResponsePayload
    public GetPlaylistsByUsuarioResponse getByUsuario(
            @RequestPayload GetPlaylistsByUsuarioRequest request) {

        GetPlaylistsByUsuarioResponse response = new GetPlaylistsByUsuarioResponse();

        Usuario usuario = usuarioRepository.findById(request.getIdUsuario()).orElse(null);

        if (usuario == null) {
            return response; // lista vazia
        }

        usuario.getPlaylistsUsuario().forEach(p -> {

            Playlist playlist = new Playlist();
            playlist.setId(p.getId());
            playlist.setNome(p.getNome());

            response.getPlaylist().add(playlist);
        });

        return response;
    }

    // =========================
    // PLAYLIST POR MÚSICA
    // =========================
    @PayloadRoot(
            namespace = NAMESPACE_URI,
            localPart = "getPlaylistsByMusicaRequest"
    )
    @ResponsePayload
    public GetPlaylistsByMusicaResponse getByMusica(@RequestPayload GetPlaylistsByMusicaRequest request) {

        GetPlaylistsByMusicaResponse response = new GetPlaylistsByMusicaResponse();

        playlistRepository.findByMusicasId(request.getIdMusica())
                .forEach(p -> {

                    Playlist playlist = new Playlist();
                    playlist.setId(p.getId());
                    playlist.setNome(p.getNome());

                    response.getPlaylist().add(playlist);
                });
        return response;
    }
}