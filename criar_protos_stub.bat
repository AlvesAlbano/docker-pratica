@echo off
setlocal EnableDelayedExpansion

REM cria diretórios de saída
mkdir grpc_stubs\java 2>nul
mkdir grpc_stubs\kotlin 2>nul

for %%L in (java kotlin) do (

    for %%P in (musica usuario playlist) do (

        if "%%L"=="java" (
            set "PROTO_DIR=servico-musica-java\java.grpc\src\main\proto"
        ) else (
            set "PROTO_DIR=servico-musica-kotlin\kotlin.grpc\src\main\proto"
        )

        echo Usando !PROTO_DIR!\%%P.proto

        python -m grpc_tools.protoc ^
        -I "!PROTO_DIR!" ^
        --python_out=grpc_stubs\%%L ^
        --grpc_python_out=grpc_stubs\%%L ^
        "!PROTO_DIR!\%%P.proto"

    )
)

echo.
echo Stubs gerados.
pause