package servico.kotlin.grpc.controller

import io.grpc.stub.StreamObserver
import org.springframework.grpc.server.service.GrpcService
import servico.kotlin.grpc.entity.Usuario
import servico.kotlin.grpc.proto.UsuarioListResponse
import servico.kotlin.grpc.proto.UsuarioRequest
import servico.kotlin.grpc.proto.UsuarioResponse
import servico.kotlin.grpc.proto.UsuarioServiceGrpc
import servico.kotlin.grpc.repository.UsuarioRepository

@GrpcService
class UsuarioController(
    private val usuarioRepository: UsuarioRepository
): UsuarioServiceGrpc.UsuarioServiceImplBase() {

    override fun todosUsuarios(
        request: UsuarioRequest?,
        responseObserver: StreamObserver<UsuarioListResponse?>
    ) {
        val usuarios: MutableList<Usuario> = usuarioRepository.findAll()

        val response: UsuarioListResponse.Builder =
            UsuarioListResponse.newBuilder()

        for (usuario in usuarios) {
            response.addUsuarios(
                UsuarioResponse.newBuilder()
                    .setId(usuario.id)
                    .setNome(usuario.nome)
                    .setIdade(usuario.idade.toInt())
                    .build()
            )
        }

        responseObserver.onNext(response.build())
        responseObserver.onCompleted()
    }
}