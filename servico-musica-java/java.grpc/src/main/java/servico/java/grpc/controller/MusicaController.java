package servico.java.grpc.controller;

import io.grpc.stub.StreamObserver;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.grpc.server.service.GrpcService;
import servico.java.grpc.entity.Musica;
import servico.java.grpc.proto.MusicaResponse;
import servico.java.grpc.proto.MusicaServiceGrpc;
import servico.java.grpc.proto.TodasMusicasRequest;
import servico.java.grpc.proto.TodasMusicasResponse;
import servico.java.grpc.repository.MusicaRepository;

import java.util.List;

@GrpcService
public class MusicaController extends MusicaServiceGrpc.MusicaServiceImplBase {

    @Autowired
    private MusicaRepository musicaRepository;

    @Override
    public void todasAsMusicas(TodasMusicasRequest request, StreamObserver<TodasMusicasResponse> responseObserver) {

        List<Musica> musicas = musicaRepository.findAll();

        TodasMusicasResponse.Builder response = TodasMusicasResponse.newBuilder();

        for (Musica musica : musicas) {

            response.addMusicas(
                    MusicaResponse.newBuilder()
                            .setId(musica.getId())
                            .setNome(musica.getNome())
                            .setArtista(musica.getArtista())
                            .build()
            );
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }
}