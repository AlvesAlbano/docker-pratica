package servico.kotlin.graphql.entity

import com.fasterxml.jackson.annotation.JsonIgnore
import jakarta.persistence.*

@Entity
class Musica {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
    var nome: String? = null
        private set
    var artista: String? = null
        private set

    @ManyToMany(mappedBy = "musicas")
    @JsonIgnore
    val playlists: MutableList<Playlist?>? = null

    protected constructor()

    constructor(nome: String?, artista: String?) {
        this.nome = nome
        this.artista = artista
    }
}