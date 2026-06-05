package servico.java.grpc.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.grpc.entity.Musica;

@Repository
public interface MusicaRepository extends JpaRepository<Musica,Long> {

}
