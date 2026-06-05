package servico.java.rest.repository;

import org.springframework.stereotype.Repository;
import servico.java.rest.entity.Musica;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface MusicaRepository extends JpaRepository<Musica,Long> {

}
