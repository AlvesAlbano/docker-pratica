package servico.java.soap.repository;

import org.springframework.stereotype.Repository;
import servico.java.soap.entity.Musica;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface MusicaRepository extends JpaRepository<Musica,Long> {

}
