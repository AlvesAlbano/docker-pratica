package servico.kotlin.rest.controller

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import servico.kotlin.rest.entity.Usuario
import servico.kotlin.rest.repository.UsuarioRepository

@RestController
@RequestMapping("/servico-rest-kotlin/usuario")
class UsuarioController {
    @Autowired
    private val usuarioRepository: UsuarioRepository? = null

    @GetMapping("/todos-usuarios")
    fun todosUsuarios(): List<Usuario> {
        return usuarioRepository!!.findAll()
    }
}
