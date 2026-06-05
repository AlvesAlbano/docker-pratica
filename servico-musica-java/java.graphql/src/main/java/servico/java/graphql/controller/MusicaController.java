package servico.java.graphql.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import servico.java.graphql.entity.Musica;
import servico.java.graphql.repository.MusicaRepository;

import java.util.List;

@Controller
public class MusicaController {

    @Autowired
    private MusicaRepository musicaRepository;

    @QueryMapping
    public List<Musica> todasAsMusicas() {
        return musicaRepository.findAll();
    }
}