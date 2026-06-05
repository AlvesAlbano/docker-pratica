package servico.java.graphql.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.graphql.entity.Musica;

@Repository
public interface MusicaRepository extends JpaRepository<Musica,Long> {

}
