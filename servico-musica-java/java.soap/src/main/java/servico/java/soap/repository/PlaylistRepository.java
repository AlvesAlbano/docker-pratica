package servico.java.soap.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.soap.entity.Playlist;

import java.util.List;

@Repository
public interface PlaylistRepository extends JpaRepository<Playlist,Long> {
    List<Playlist> findByMusicasId(Long idMusica);
}
