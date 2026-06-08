package servico.kotlin.soap.config

import org.springframework.boot.web.servlet.ServletRegistrationBean
import org.springframework.context.ApplicationContext
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.io.ClassPathResource
import org.springframework.ws.config.annotation.EnableWs
import org.springframework.ws.transport.http.MessageDispatcherServlet
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition
import org.springframework.xml.xsd.SimpleXsdSchema
import org.springframework.xml.xsd.XsdSchema

@EnableWs
@Configuration
class WebServiceConfig {
    @Bean
    fun messageDispatcherServlet(context: ApplicationContext): ServletRegistrationBean<MessageDispatcherServlet> {
        val servlet = MessageDispatcherServlet()
        servlet.setApplicationContext(context)
        servlet.isTransformWsdlLocations = true
        return ServletRegistrationBean(servlet, "/ws/*")
    }

    @Bean(name = ["musica"])
    fun todasMusicasWsd(musicaSchema: XsdSchema): DefaultWsdl11Definition {
        val wsdl = DefaultWsdl11Definition()
        wsdl.setPortTypeName("MusicaPort")
        wsdl.setLocationUri("/ws")
        wsdl.setTargetNamespace("http://soap.kotlin.servico/musica")
        wsdl.setSchema(musicaSchema)
        return wsdl
    }

    @Bean(name = ["playlist"])
    fun playlistMusicaIdWsd(playlistSchema: XsdSchema): DefaultWsdl11Definition {
        val wsdl = DefaultWsdl11Definition()
        wsdl.setPortTypeName("PlaylistPort")
        wsdl.setLocationUri("/ws")
        wsdl.setTargetNamespace("http://soap.kotlin.servico/playlist")
        wsdl.setSchema(playlistSchema)
        return wsdl
    }

    @Bean(name = ["usuario"])
    fun todosUsuariosWsd(usuarioSchema: XsdSchema): DefaultWsdl11Definition {
        val wsdl = DefaultWsdl11Definition()
        wsdl.setPortTypeName("UsuarioPort")
        wsdl.setLocationUri("/ws")
        wsdl.setTargetNamespace("http://soap.kotlin.servico/usuario")
        wsdl.setSchema(usuarioSchema)
        return wsdl
    }

    @Bean
    fun musicaSchema(): XsdSchema {
        return SimpleXsdSchema(ClassPathResource("xsd/musica.xsd"))
    }

    @Bean
    fun usuarioSchema(): XsdSchema {
        return SimpleXsdSchema(ClassPathResource("xsd/usuario.xsd"))
    }

    @Bean
    fun playlistSchema(): XsdSchema {
        return SimpleXsdSchema(ClassPathResource("xsd/playlist.xsd"))
    }
}