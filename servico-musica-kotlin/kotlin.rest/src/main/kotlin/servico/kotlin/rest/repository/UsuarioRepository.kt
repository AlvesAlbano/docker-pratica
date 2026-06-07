package servico.kotlin.rest.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.rest.entity.Usuario

@Repository
interface UsuarioRepository : JpaRepository<Usuario, Long>
