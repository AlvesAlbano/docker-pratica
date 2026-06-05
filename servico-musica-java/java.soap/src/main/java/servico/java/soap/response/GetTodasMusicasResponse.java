package servico.java.soap.response;

import servico.java.soap.DTO.MusicaSoap;

import java.util.List;

public class GetTodasMusicasResponse {
    private List<MusicaSoap> musicas;

    public List<MusicaSoap> getMusicas() {
        return musicas;
    }

    public void setMusicas(List<MusicaSoap> musicas) {
        this.musicas = musicas;
    }
}