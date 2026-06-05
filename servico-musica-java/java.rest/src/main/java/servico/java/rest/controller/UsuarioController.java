package servico.java.rest.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import servico.java.rest.entity.Usuario;
import servico.java.rest.repository.UsuarioRepository;

import java.util.List;

@RestController
@RequestMapping("/servico-rest-java/usuario")
public class UsuarioController {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @GetMapping("/todos-usuarios")
    public List<Usuario> todosUsuarios(){
        return usuarioRepository.findAll();
    }
}
