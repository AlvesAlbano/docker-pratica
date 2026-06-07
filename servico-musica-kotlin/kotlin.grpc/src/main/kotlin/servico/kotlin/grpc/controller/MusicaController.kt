package servico.kotlin.grpc.controller

import io.grpc.stub.StreamObserver
import org.springframework.grpc.server.service.GrpcService
import servico.kotlin.grpc.entity.Musica
import servico.kotlin.grpc.proto.MusicaResponse
import servico.kotlin.grpc.proto.MusicaServiceGrpc
import servico.kotlin.grpc.proto.TodasMusicasRequest
import servico.kotlin.grpc.proto.TodasMusicasResponse
import servico.kotlin.grpc.repository.MusicaRepository

@GrpcService
class MusicaController(
    private val musicaRepository: MusicaRepository
) : MusicaServiceGrpc.MusicaServiceImplBase() {

    override fun todasAsMusicas(
        request: TodasMusicasRequest?,
        responseObserver: StreamObserver<TodasMusicasResponse?>
    ) {
        val musicas: MutableList<Musica> = musicaRepository.findAll()

        val response: TodasMusicasResponse.Builder =
            TodasMusicasResponse.newBuilder()

        for (musica in musicas) {
            response.addMusicas(
                MusicaResponse.newBuilder()
                    .setId(musica.id)
                    .setNome(musica.nome)
                    .setArtista(musica.artista)
                    .build()
            )
        }

        responseObserver.onNext(response.build())
        responseObserver.onCompleted()
    }
}