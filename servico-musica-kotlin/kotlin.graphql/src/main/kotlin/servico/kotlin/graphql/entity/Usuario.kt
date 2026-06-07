package servico.kotlin.graphql.entity

import jakarta.persistence.*

@Entity
class Usuario {
//    @JvmField
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
    var nome: String? = null
        private set
    var idade: Short = 0
        private set

    @OneToMany(mappedBy = "usuario", cascade = [CascadeType.ALL])
    val playlistsUsuario: MutableList<Playlist?> = ArrayList<Playlist?>()

    protected constructor()

    constructor(nome: String?, idade: Short) {
        this.nome = nome
        this.idade = idade
    }
}
