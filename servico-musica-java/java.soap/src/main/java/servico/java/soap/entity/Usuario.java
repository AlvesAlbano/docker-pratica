package servico.java.soap.entity;

import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.List;

@Entity
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    private String nome;
    private short idade;

    @OneToMany(mappedBy = "usuario",cascade = CascadeType.ALL)
    private List<Playlist> playlistsUsuario = new ArrayList<>();

    protected Usuario(){}

    public Usuario(String nome, short idade) {
        this.nome = nome;
        this.idade = idade;
    }

    public long getId() {
        return id;
    }

    public String getNome() {
        return nome;
    }

    public short getIdade() {
        return idade;
    }

    public List<Playlist> getPlaylistsUsuario() {
        return playlistsUsuario;
    }
}
