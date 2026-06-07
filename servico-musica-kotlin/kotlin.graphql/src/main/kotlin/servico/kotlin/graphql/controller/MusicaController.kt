package servico.kotlin.graphql.controller

import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller
import servico.kotlin.graphql.entity.Musica
import servico.kotlin.graphql.repository.MusicaRepository

@Controller
class MusicaController (
    private val musicaRepository: MusicaRepository
) {

    @QueryMapping
    fun todasAsMusicas(): List<Musica> {
        return musicaRepository.findAll()
    }
}