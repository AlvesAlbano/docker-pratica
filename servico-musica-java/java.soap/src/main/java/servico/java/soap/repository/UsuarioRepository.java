package servico.java.soap.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.soap.entity.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario,Long> {
}
