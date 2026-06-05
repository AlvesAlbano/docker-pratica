package servico.java.soap.response;

import servico.java.soap.DTO.UsuarioSoap;

import java.util.List;

public class GetTodosUsuariosResponse {

    private List<UsuarioSoap> usuario;

    public List<UsuarioSoap> getUsuario() {
        return usuario;
    }

    public void setUsuario(List<UsuarioSoap> usuario) {
        this.usuario = usuario;
    }
}