package servico.java.rest.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

import java.util.List;

@Entity
public class Musica {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    private String nome;
    private String artista;

    @ManyToMany(mappedBy = "musicas")
    @JsonIgnore
    private List<Playlist> playlists;

    protected Musica() {
    }

    public Musica(String nome, String artista) {
        this.nome = nome;
        this.artista = artista;
    }

    public long getId() {
        return id;
    }

    public String getNome() {
        return nome;
    }

    public String getArtista() {
        return artista;
    }

    public List<Playlist> getPlaylists() {
        return playlists;
    }
}