package servico.kotlin.soap.entity

import com.fasterxml.jackson.annotation.JsonIgnore
import jakarta.persistence.*

@Entity
class Playlist {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    var nome: String? = null

    @ManyToMany
    val musicas: MutableList<Musica?> = ArrayList()

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    @JsonIgnore
    var usuario: Usuario? = null

    protected constructor()

    constructor(nome: String?) {
        this.nome = nome
    }
}