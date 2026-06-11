#!/bin/bash
set -x
# cria diretórios de saída
mkdir -p ./locust/grpc_stubs/java
mkdir -p ./locust/grpc_stubs/kotlin

for L in java kotlin; do

    for P in musica usuario playlist; do

        if [ "$L" = "java" ]; then
            PROTO_DIR="servico-musica-java/java.grpc/src/main/proto"
        else
            PROTO_DIR="servico-musica-kotlin/kotlin.grpc/src/main/proto"
        fi

        echo "Usando ${PROTO_DIR}/${P}.proto"

        python -m grpc_tools.protoc \
            -I "$PROTO_DIR" \
            --python_out="./locust/grpc_stubs/$L" \
            --grpc_python_out="./locust/grpc_stubs/$L" \
            "$PROTO_DIR/$P.proto"

    done

done

echo
echo "Stubs gerados."