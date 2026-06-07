package servico.kotlin.soap.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.soap.entity.Playlist

@Repository
interface PlaylistRepository : JpaRepository<Playlist, Long> {
    fun findByMusicasId(idMusica: Long?): MutableList<Playlist?>?
}
