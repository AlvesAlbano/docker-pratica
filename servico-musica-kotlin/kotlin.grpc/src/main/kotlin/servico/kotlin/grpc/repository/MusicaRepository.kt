package servico.kotlin.grpc.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.grpc.entity.Musica

@Repository
interface MusicaRepository : JpaRepository<Musica, Long>
