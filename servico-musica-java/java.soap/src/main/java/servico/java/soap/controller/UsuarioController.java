package servico.java.soap.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import servico.java.soap.DTO.UsuarioSoap;
import servico.java.soap.repository.UsuarioRepository;
import servico.java.soap.request.GetTodosUsuariosRequest;
import servico.java.soap.response.GetTodosUsuariosResponse;

import java.util.List;

@Endpoint
public class UsuarioController {

    private static final String NAMESPACE_URI = "http://soap.java.servico/usuario";

    private final UsuarioRepository usuarioRepository;

    public UsuarioController(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getTodosUsuariosRequest")
    @ResponsePayload
    public GetTodosUsuariosResponse getTodosUsuarios(@RequestPayload GetTodosUsuariosRequest request) {

        List<UsuarioSoap> usuarios = usuarioRepository.findAll()
                .stream()
                .map(u -> {
                    UsuarioSoap dto = new UsuarioSoap();
                    dto.setId(u.getId());
                    dto.setNome(u.getNome());
                    dto.setIdade(u.getIdade());
                    return dto;
                })
                .toList();

        GetTodosUsuariosResponse response = new GetTodosUsuariosResponse();
        response.setUsuario(usuarios);

        return response;
    }
}