package servico.java.rest.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import servico.java.rest.entity.Musica;
import servico.java.rest.repository.MusicaRepository;

import java.util.List;

@RestController
@RequestMapping("/servico-rest-java/musica")
public class MusicaController {

    @Autowired
    private MusicaRepository musicaRepository;

    @GetMapping("/todas-musicas")
    public List<Musica> todasAsMusicas(){
        return musicaRepository.findAll();
    }
}