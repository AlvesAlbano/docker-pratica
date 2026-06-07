package servico.kotlin.soap.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.soap.entity.Usuario

@Repository
interface UsuarioRepository : JpaRepository<Usuario, Long>
