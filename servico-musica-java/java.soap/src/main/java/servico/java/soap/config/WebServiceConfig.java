package servico.java.soap.config;

import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.ws.config.annotation.EnableWs;
import org.springframework.ws.transport.http.MessageDispatcherServlet;
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition;
import org.springframework.xml.xsd.SimpleXsdSchema;
import org.springframework.xml.xsd.XsdSchema;

@EnableWs
@Configuration
public class WebServiceConfig {

    @Bean
    public ServletRegistrationBean<MessageDispatcherServlet> messageDispatcherServlet(ApplicationContext context) {
        MessageDispatcherServlet servlet = new MessageDispatcherServlet();
        servlet.setApplicationContext(context);
        servlet.setTransformWsdlLocations(true);
        return new ServletRegistrationBean<>(servlet, "/ws/*");
    }

    @Bean(name = "musica")
    public DefaultWsdl11Definition todasMusicasWsd (XsdSchema musicaSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("MusicaPort");
        wsdl.setLocationUri("/ws");
        wsdl.setTargetNamespace("http://soap.java.servico/musica");
        wsdl.setSchema(musicaSchema);
        return wsdl;
    }

    @Bean(name = "playlist")
    public DefaultWsdl11Definition playlistMusicaIdWsd (XsdSchema playlistSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("PlaylistPort");
        wsdl.setLocationUri("/ws");
        wsdl.setTargetNamespace("http://soap.java.servico/playlist");
        wsdl.setSchema(playlistSchema);
        return wsdl;
    }

    @Bean(name = "usuario")
    public DefaultWsdl11Definition todosUsuariosWsd (XsdSchema usuarioSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("UsuarioPort");
        wsdl.setLocationUri("/ws");
        wsdl.setTargetNamespace("http://soap.java.servico/usuario");
        wsdl.setSchema(usuarioSchema);
        return wsdl;
    }

    @Bean
    public XsdSchema musicaSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/musica.xsd"));
    }

    @Bean
    public XsdSchema usuarioSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/usuario.xsd"));
    }

    @Bean
    public XsdSchema playlistSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/playlist.xsd"));
    }
}