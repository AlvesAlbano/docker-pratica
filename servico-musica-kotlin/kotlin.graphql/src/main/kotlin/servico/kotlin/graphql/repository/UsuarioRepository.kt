package servico.kotlin.graphql.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import servico.kotlin.graphql.entity.Usuario

@Repository
interface UsuarioRepository : JpaRepository<Usuario, Long>
