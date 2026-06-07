package servico.kotlin.graphql

import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication

@SpringBootApplication
object Application {
    @kotlin.jvm.JvmStatic
    fun main(args: Array<String>) {
        SpringApplication.run(Application::class.java, *args)
        println("http://localhost:8080/graphiql")
    }
}
