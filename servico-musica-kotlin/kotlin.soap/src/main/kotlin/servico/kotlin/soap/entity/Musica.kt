package servico.kotlin.soap.entity

import com.fasterxml.jackson.annotation.JsonIgnore
import jakarta.persistence.*

@Entity
class Musica {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    var nome: String? = null

    var artista: String? = null

    @ManyToMany(mappedBy = "musicas")
    @JsonIgnore
    var playlists: MutableList<Playlist> = mutableListOf()

    protected constructor()

    constructor(nome: String?, artista: String?) {
        this.nome = nome
        this.artista = artista
    }
}