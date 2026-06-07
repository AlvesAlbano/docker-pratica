package servico.kotlin.graphql.controller

import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller
import servico.kotlin.graphql.entity.Usuario
import servico.kotlin.graphql.repository.UsuarioRepository

@Controller
class UsuarioController(private val usuarioRepository: UsuarioRepository) {
    @QueryMapping
    fun todosUsuarios(): MutableList<Usuario> {
        return usuarioRepository.findAll()
    }
}