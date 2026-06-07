package servico.kotlin.grpc.controller

import io.grpc.stub.StreamObserver
import jakarta.transaction.Transactional
import org.springframework.grpc.server.service.GrpcService
import servico.kotlin.grpc.entity.Playlist
import servico.kotlin.grpc.entity.Usuario
import servico.kotlin.grpc.proto.*
import servico.kotlin.grpc.repository.PlaylistRepository
import servico.kotlin.grpc.repository.UsuarioRepository
import java.util.*

@GrpcService
class PlaylistController(
    private val playlistRepository: PlaylistRepository,
    private val usuarioRepository: UsuarioRepository
) : PlaylistServiceGrpc.PlaylistServiceImplBase() {

    @Transactional
    override fun playlistsPorUsuario(
        request: PlaylistPorUsuarioRequest,
        responseObserver: StreamObserver<PlaylistListResponse>
    ) {

        val response = PlaylistListResponse.newBuilder()

        val usuario: Optional<Usuario> =
            usuarioRepository.findById(request.idUsuario)

        if (usuario.isPresent) {
            usuario.get().playlistsUsuario.forEach { playlist ->
                response.addPlaylists(
                    PlaylistResponse.newBuilder()
                        .setId(playlist.id)
                        .setNome(playlist.nome)
                        .build()
                )
            }
        }

        responseObserver.onNext(response.build())
        responseObserver.onCompleted()
    }

    override fun playlistsPorMusica(
        request: PlaylistPorMusicaRequest,
        responseObserver: StreamObserver<PlaylistListResponse>
    ) {

        val playlists: List<Playlist> =
            playlistRepository.findByMusicasId(request.idMusica)

        val response = PlaylistListResponse.newBuilder()

        playlists.forEach { playlist ->
            response.addPlaylists(
                PlaylistResponse.newBuilder()
                    .setId(playlist.id)
                    .setNome(playlist.nome)
                    .build()
            )
        }

        responseObserver.onNext(response.build())
        responseObserver.onCompleted()
    }
}