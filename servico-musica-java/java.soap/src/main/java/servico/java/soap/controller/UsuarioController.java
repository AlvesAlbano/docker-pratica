package servico.java.soap.controller;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import servico.java.soap.generated.*;
import servico.java.soap.repository.UsuarioRepository;

@Endpoint
public class UsuarioController {

    private static final String NAMESPACE_URI =
            "http://soap.java.servico/usuario";

    private final UsuarioRepository usuarioRepository;

    public UsuarioController(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    @PayloadRoot(
            namespace = NAMESPACE_URI,
            localPart = "getTodosUsuariosRequest"
    )
    @ResponsePayload
    public GetTodosUsuariosResponse getTodosUsuarios( @RequestPayload GetTodosUsuariosRequest request) {

        GetTodosUsuariosResponse response = new GetTodosUsuariosResponse();

        usuarioRepository.findAll().forEach(u -> {

            Usuario usuario = new Usuario();
            usuario.setId(u.getId());
            usuario.setNome(u.getNome());
            usuario.setIdade(u.getIdade());

            response.getUsuario().add(usuario);
        });

        return response;
    }
}