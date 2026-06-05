package servico.java.soap.controller;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import servico.java.soap.DTO.MusicaSoap;
import servico.java.soap.entity.Musica;
import servico.java.soap.repository.MusicaRepository;
import servico.java.soap.response.GetTodasMusicasResponse;

import java.util.List;

@Endpoint
public class MusicaController {

    private static final String NAMESPACE_URI = "http://soap.java.servico/musica";

    private final MusicaRepository musicaRepository;

    public MusicaController(MusicaRepository musicaRepository) {
        this.musicaRepository = musicaRepository;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getTodasMusicasRequest")
    @ResponsePayload
    public GetTodasMusicasResponse getTodasMusicas() {

        GetTodasMusicasResponse response = new GetTodasMusicasResponse();

        List<Musica> musicas = musicaRepository.findAll();

        List<MusicaSoap> musicaSoapList = musicas.stream().map(m -> {
            MusicaSoap soap = new MusicaSoap();
            soap.setId(m.getId());
            soap.setNome(m.getNome());
            soap.setArtista(m.getArtista());
            return soap;
        }).toList();

        response.setMusicas(musicaSoapList);

        return response;
    }
}