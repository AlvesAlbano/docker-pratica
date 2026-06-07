package servico.java.soap.controller;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import servico.java.soap.generated.GetTodasMusicasRequest;
import servico.java.soap.generated.GetTodasMusicasResponse;
import servico.java.soap.repository.MusicaRepository;
import servico.java.soap.generated.Musica;

@Endpoint
public class MusicaController {

    private static final String NAMESPACE_URI = "http://soap.java.servico/musica";

    private final MusicaRepository musicaRepository;

    public MusicaController(MusicaRepository musicaRepository) {
        this.musicaRepository = musicaRepository;
    }

    @PayloadRoot(
            namespace = NAMESPACE_URI,
            localPart = "getTodasMusicasRequest"
    )
    @ResponsePayload
    public GetTodasMusicasResponse getTodasMusicas(
            @RequestPayload GetTodasMusicasRequest request) {

        GetTodasMusicasResponse response =
                new GetTodasMusicasResponse();

        musicaRepository.findAll().forEach(m -> {

            Musica soapMusica = new servico.java.soap.generated.Musica();

            soapMusica.setId(m.getId());
            soapMusica.setNome(m.getNome());
            soapMusica.setArtista(m.getArtista());

            response.getMusica().add(soapMusica);
        });

        return response;
    }
}