package servico.java.grpc.controller;

import io.grpc.stub.StreamObserver;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.grpc.server.service.GrpcService;

import servico.java.grpc.entity.Usuario;
import servico.java.grpc.proto.UsuarioListResponse;
import servico.java.grpc.proto.UsuarioRequest;
import servico.java.grpc.proto.UsuarioResponse;
import servico.java.grpc.proto.UsuarioServiceGrpc;
import servico.java.grpc.repository.UsuarioRepository;

import java.util.List;

@GrpcService
public class UsuarioController extends UsuarioServiceGrpc.UsuarioServiceImplBase {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Override
    public void todosUsuarios(UsuarioRequest request, StreamObserver<UsuarioListResponse> responseObserver) {

        List<Usuario> usuarios = usuarioRepository.findAll();

        UsuarioListResponse.Builder response = UsuarioListResponse.newBuilder();

        for (Usuario usuario : usuarios) {
            response.addUsuarios(
                    UsuarioResponse.newBuilder()
                            .setId(usuario.getId())
                            .setNome(usuario.getNome())
                            .setIdade(usuario.getIdade())
                            .build()
            );
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }
}