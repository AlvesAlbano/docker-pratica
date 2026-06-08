package servico.kotlin.grpc.entity

import jakarta.persistence.*

@Entity
class Musica {
//    @JvmField
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
    var nome: String? = null
        private set
    var artista: String? = null
        private set

    @ManyToMany(mappedBy = "musicas")
    val playlists: MutableList<Playlist> = ArrayList()

    protected constructor()

    constructor(nome: String?, artista: String?) {
        this.nome = nome
        this.artista = artista
    }
}