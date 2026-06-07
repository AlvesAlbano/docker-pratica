package servico.kotlin.graphql.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.graphql.entity.Musica

@Repository
interface MusicaRepository : JpaRepository<Musica, Long>
