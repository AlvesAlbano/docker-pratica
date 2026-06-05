package servico.java.soap.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import servico.java.soap.DTO.PlaylistSoap;
import servico.java.soap.entity.Usuario;
import servico.java.soap.repository.PlaylistRepository;
import servico.java.soap.repository.UsuarioRepository;
import servico.java.soap.request.GetPlaylistsByMusicaRequest;
import servico.java.soap.request.GetPlaylistsByUsuarioRequest;
import servico.java.soap.response.GetPlaylistsByMusicaResponse;
import servico.java.soap.response.GetPlaylistsByUsuarioResponse;

import java.util.List;
import java.util.Optional;

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
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getPlaylistsByUsuarioRequest")
    @ResponsePayload
    public GetPlaylistsByUsuarioResponse getByUsuario(@RequestPayload GetPlaylistsByUsuarioRequest request) {

        GetPlaylistsByUsuarioResponse response = new GetPlaylistsByUsuarioResponse();

        Optional<Usuario> usuario = usuarioRepository.findById(request.getIdUsuario());

        if (usuario.isEmpty()) {
            response.setPlaylist(List.of());
            return response;
        }

        List<PlaylistSoap> playlists = usuario.get()
                .getPlaylistsUsuario()
                .stream()
                .map(p -> {
                    PlaylistSoap dto = new PlaylistSoap();
                    dto.setId(p.getId());
                    dto.setNome(p.getNome());
                    return dto;
                })
                .toList();

        response.setPlaylist(playlists);
        return response;
    }

    // =========================
    // PLAYLIST POR MÚSICA
    // =========================
    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getPlaylistsByMusicaRequest")
    @ResponsePayload
    public GetPlaylistsByMusicaResponse getByMusica(@RequestPayload GetPlaylistsByMusicaRequest request) {

        GetPlaylistsByMusicaResponse response = new GetPlaylistsByMusicaResponse();

        List<PlaylistSoap> playlists = playlistRepository
                .findByMusicasId(request.getIdMusica())
                .stream()
                .map(p -> {
                    PlaylistSoap dto = new PlaylistSoap();
                    dto.setId(p.getId());
                    dto.setNome(p.getNome());
                    return dto;
                })
                .toList();

        response.setPlaylist(playlists);

        return response;
    }
}