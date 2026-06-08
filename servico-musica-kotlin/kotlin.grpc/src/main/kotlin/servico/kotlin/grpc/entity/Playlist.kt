package servico.kotlin.grpc.entity

import jakarta.persistence.*

@Entity
class Playlist {
//    @JvmField
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
    var nome: String? = null
        private set

//    @JvmField
    @ManyToMany
    val musicas: MutableList<Musica> = ArrayList()

//    @JvmField
    @ManyToOne
    @JoinColumn(name = "usuario_id")
    var usuario: Usuario? = null

    protected constructor()

    constructor(nome: String?) {
        this.nome = nome
    }
}