package servico.kotlin.rest.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.rest.entity.Musica

@Repository
interface MusicaRepository : JpaRepository<Musica, Long>
