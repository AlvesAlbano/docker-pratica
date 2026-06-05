package servico.java.grpc.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import servico.java.grpc.entity.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario,Long> {
}
