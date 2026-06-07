package servico.kotlin.grpc.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.grpc.entity.Usuario

@Repository
interface UsuarioRepository : JpaRepository<Usuario, Long>
