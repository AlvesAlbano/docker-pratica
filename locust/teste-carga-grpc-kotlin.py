import time
import random

import grpc
from locust import User, task, between, events

import sys

sys.path.insert(0, "/mnt/locust/grpc_stubs/kotlin")

from grpc_stubs.kotlin import musica_pb2
from grpc_stubs.kotlin import musica_pb2_grpc

from grpc_stubs.kotlin import playlist_pb2
from grpc_stubs.kotlin import playlist_pb2_grpc

from grpc_stubs.kotlin import usuario_pb2
from grpc_stubs.kotlin import usuario_pb2_grpc

class GrpcUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        self.channel = grpc.insecure_channel("kotlin-grpc:8086")

        self.musica_client = musica_pb2_grpc.MusicaServiceStub(self.channel)
        self.playlist_client = playlist_pb2_grpc.PlaylistServiceStub(self.channel)
        self.usuario_client = usuario_pb2_grpc.UsuarioServiceStub(self.channel)

    # 1 - grpcurl -d '{}' MusicaService/TodasAsMusicas
    @task
    def todas_as_musicas(self):
        request = musica_pb2.TodasMusicasRequest()

        start = time.perf_counter()

        try:
            response = self.musica_client.TodasAsMusicas(request)

            events.request.fire(
                request_type="gRPC",
                name="MusicaService/TodasAsMusicas",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=response.ByteSize(),
                exception=None,
            )

        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name="MusicaService/TodasAsMusicas",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=0,
                exception=e,
            )

    # 2 - grpcurl -d '{"idUsuario":8}' PlaylistService/PlaylistsPorUsuario
    @task
    def playlists_por_usuario(self):
        request = playlist_pb2.PlaylistPorUsuarioRequest(
            idUsuario=8
        )

        start = time.perf_counter()

        try:
            response = self.playlist_client.PlaylistsPorUsuario(request)

            events.request.fire(
                request_type="gRPC",
                name="PlaylistService/PlaylistsPorUsuario",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=response.ByteSize(),
                exception=None,
            )

        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name="PlaylistService/PlaylistsPorUsuario",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=0,
                exception=e,
            )

    # 3 - grpcurl -d '{"idMusica": 1}' PlaylistService/PlaylistsPorMusica
    @task
    def playlists_por_musica(self):
        request = playlist_pb2.PlaylistPorMusicaRequest(
            idMusica=1
        )

        start = time.perf_counter()

        try:
            response = self.playlist_client.PlaylistsPorMusica(request)

            events.request.fire(
                request_type="gRPC",
                name="PlaylistService/PlaylistsPorMusica",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=response.ByteSize(),
                exception=None,
            )

        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name="PlaylistService/PlaylistsPorMusica",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=0,
                exception=e,
            )

    # 4 - grpcurl -d '{}' UsuarioService/TodosUsuarios
    @task
    def todos_usuarios(self):
        request = usuario_pb2.UsuarioRequest()

        start = time.perf_counter()

        try:
            response = self.usuario_client.TodosUsuarios(request)

            events.request.fire(
                request_type="gRPC",
                name="UsuarioService/TodosUsuarios",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=response.ByteSize(),
                exception=None,
            )

        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name="UsuarioService/TodosUsuarios",
                response_time=(time.perf_counter() - start) * 1000,
                response_length=0,
                exception=e,
            )