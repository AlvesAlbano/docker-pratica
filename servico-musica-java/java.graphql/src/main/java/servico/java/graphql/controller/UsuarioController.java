package servico.java.graphql.controller;

import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import servico.java.graphql.entity.Usuario;
import servico.java.graphql.repository.UsuarioRepository;

import java.util.List;

@Controller
public class UsuarioController {

    private final UsuarioRepository usuarioRepository;

    public UsuarioController(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    @QueryMapping
    public List<Usuario> todosUsuarios() {
        return usuarioRepository.findAll();
    }
}