package servico.java.soap.response;

import servico.java.soap.DTO.PlaylistSoap;

import java.util.List;

public class GetPlaylistsByMusicaResponse {
    private List<PlaylistSoap> playlist;

    public List<PlaylistSoap> getPlaylist() {
        return playlist;
    }

    public void setPlaylist(List<PlaylistSoap> playlist) {
        this.playlist = playlist;
    }
}
