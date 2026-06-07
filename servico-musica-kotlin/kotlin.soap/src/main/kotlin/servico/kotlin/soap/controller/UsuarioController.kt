package servico.kotlin.soap.controller

import org.springframework.ws.server.endpoint.annotation.*
import servico.kotlin.soap.generated.*
import servico.kotlin.soap.repository.UsuarioRepository

@Endpoint
class UsuarioController(
    private val usuarioRepository: UsuarioRepository
) {

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getTodosUsuariosRequest")
    @ResponsePayload
    fun getTodosUsuarios(
        @RequestPayload request: GetTodosUsuariosRequest?
    ): GetTodosUsuariosResponse {

        val response = GetTodosUsuariosResponse()

        usuarioRepository.findAll().forEach { u ->
            val usuario = Usuario().apply {
                id = u.id!!
                nome = u.nome
                idade = u.idade
            }

            response.usuario.add(usuario)
        }

        return response
    }

    companion object {
        private const val NAMESPACE_URI = "http://soap.kotlin.servico/usuario"
    }
}