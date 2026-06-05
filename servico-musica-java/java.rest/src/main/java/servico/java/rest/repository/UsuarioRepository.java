package servico.java.rest.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.rest.entity.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario,Long> {
}
