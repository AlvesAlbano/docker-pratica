package servico.kotlin.grpc.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.grpc.entity.Playlist

@Repository
interface PlaylistRepository : JpaRepository<Playlist, Long> {
    fun findByMusicasId(idMusica: Long?): MutableList<Playlist>
}
