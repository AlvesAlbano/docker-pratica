package servico.java.rest.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.rest.entity.Musica;

@Repository
public interface MusicaRepository extends JpaRepository<Musica,Long> {

}
