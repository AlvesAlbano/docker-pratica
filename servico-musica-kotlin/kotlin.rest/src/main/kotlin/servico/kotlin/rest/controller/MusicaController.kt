package servico.kotlin.rest.controller

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import servico.kotlin.rest.entity.Musica
import servico.kotlin.rest.repository.MusicaRepository

@RestController
@RequestMapping("/servico-rest-kotlin/musica")
class MusicaController {
    @Autowired
    private val musicaRepository: MusicaRepository? = null

    @GetMapping("/todas-musicas")
    fun todasAsMusicas(): List<Musica> {
        return musicaRepository!!.findAll()
    }
}