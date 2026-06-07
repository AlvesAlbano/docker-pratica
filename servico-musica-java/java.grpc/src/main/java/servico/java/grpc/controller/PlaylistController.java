package servico.java.grpc.controller;

import io.grpc.stub.StreamObserver;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.grpc.server.service.GrpcService;

import servico.java.grpc.entity.Playlist;
import servico.java.grpc.entity.Usuario;
import servico.java.grpc.proto.PlaylistListResponse;
import servico.java.grpc.proto.PlaylistResponse;
import servico.java.grpc.proto.PlaylistServiceGrpc;
import servico.java.grpc.proto.PlaylistPorUsuarioRequest;
import servico.java.grpc.proto.PlaylistPorMusicaRequest;
import servico.java.grpc.repository.PlaylistRepository;
import servico.java.grpc.repository.UsuarioRepository;

import java.util.List;
import java.util.Optional;

@GrpcService
public class PlaylistController extends PlaylistServiceGrpc.PlaylistServiceImplBase {

    @Autowired
    private PlaylistRepository playlistRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Transactional
    @Override
    public void playlistsPorUsuario(PlaylistPorUsuarioRequest request, StreamObserver<PlaylistListResponse> responseObserver) {

        PlaylistListResponse.Builder response = PlaylistListResponse.newBuilder();

        Optional<Usuario> usuario = usuarioRepository.findById(request.getIdUsuario());

        if (usuario.isPresent()) {
            for (Playlist playlist : usuario.get().getPlaylistsUsuario()) {

                response.addPlaylists(
                        PlaylistResponse.newBuilder()
                                .setId(playlist.getId())
                                .setNome(playlist.getNome())
                                .build()
                );
            }
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }

    @Override
    public void playlistsPorMusica(PlaylistPorMusicaRequest request, StreamObserver<PlaylistListResponse> responseObserver) {

        List<Playlist> playlists = playlistRepository.findByMusicasId(request.getIdMusica());

        PlaylistListResponse.Builder response = PlaylistListResponse.newBuilder();

        for (Playlist playlist : playlists) {
            response.addPlaylists(
                    PlaylistResponse.newBuilder()
                            .setId(playlist.getId())
                            .setNome(playlist.getNome())
                            .build()
            );
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }
}