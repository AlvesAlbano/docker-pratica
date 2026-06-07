package servico.kotlin.soap.entity

import jakarta.persistence.*

@Entity
class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    var nome: String? = null

    var idade: Short = 0

    @OneToMany(mappedBy = "usuario", cascade = [CascadeType.ALL])
    var playlistsUsuario: MutableList<Playlist> = mutableListOf()

    constructor()

    constructor(nome: String?, idade: Short) {
        this.nome = nome
        this.idade = idade
    }
}