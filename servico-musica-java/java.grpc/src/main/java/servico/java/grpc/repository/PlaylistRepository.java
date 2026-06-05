package servico.java.grpc.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.grpc.entity.Playlist;

import java.util.List;

@Repository
public interface PlaylistRepository extends JpaRepository<Playlist,Long> {
    List<Playlist> findByMusicasId(Long idMusica);
}
