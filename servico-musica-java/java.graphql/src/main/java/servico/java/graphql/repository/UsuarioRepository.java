package servico.java.graphql.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.graphql.entity.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario,Long> {
}
