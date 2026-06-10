#!/bin/bash

tipo_teste=("leve" "medio" "pesado")
tipo_api=("rest" "soap" "graphql")

u=(100 200 300)
r=(15 30 75)

api_url_java=(
  "http://java-rest:8080"
  "http://java-soap:8081"
  "http://java-graphql:8083"
)

# JAVA LOCUST
for j in "${!tipo_teste[@]}"; do
  for x in "${!tipo_api[@]}"; do
    docker compose run --rm locust -f "teste-carga-${tipo_api[$x]}-java.py" \
      --host="${api_url_java[$x]}" \
      --headless \
      -u "${u[$j]}" \
      -r "${r[$j]}" \
      -t 1m \
      --csv="./resultados/${tipo_teste[$j]}/api-${tipo_api[$x]}-java/api-${tipo_api[$x]}-java_${tipo_teste[$j]}_u${u[$j]}_r${r[$j]}"
  done
done

api_url_kotlin=(
  "http://kotlin-rest:8084"
  "http://kotlin-soap:8085"
  "http://kotlin-graphql:8087"
)

# KOTLIN LOCUST
for j in "${!tipo_teste[@]}"; do
  for x in "${!tipo_api[@]}"; do
    docker compose run --rm locust -f "teste-carga-${tipo_api[$x]}-kotlin.py" \
      --host="${api_url_kotlin[$x]}" \
      --headless \
      -u "${u[$j]}" \
      -r "${r[$j]}" \
      -t 1m \
      --csv="./resultados/${tipo_teste[$j]}/api-${tipo_api[$x]}-kotlin/api-${tipo_api[$x]}-kotlin_${tipo_teste[$j]}_u${u[$j]}_r${r[$j]}"
  done
done

linguagem=("java" "kotlin")

grpc_get=(
  "MusicaService.TodasAsMusicas musica"
  "UsuarioService.TodosUsuarios usuario"
)

grpc_post=(
  'PlaylistService.PlaylistsPorUsuario playlist {"idUsuario": 8}'
  'PlaylistService.PlaylistsPorMusica playlist {"idMusica": 8}'
)

grpc_users=(100 200 300)

mkdir -p resultados-grpc/{leve,medio,pesado}/api-grpc-java
mkdir -p resultados-grpc/{leve,medio,pesado}/api-grpc-kotlin

# sudo chown -R $USER:$USER resultados-grpc/{leve,medio,pesado}/api-grpc-java
# sudo chown -R $USER:$USER resultados-grpc/{leve,medio,pesado}/api-grpc-kotlin

# GRPC GET
for a in "${!linguagem[@]}"; do
  for j in "${!tipo_teste[@]}"; do
    for s in "${!grpc_get[@]}"; do

      linguagem_atual="${linguagem[$a]}"
      service=$(echo "${grpc_get[$s]}" | awk '{print $1}')
      proto=$(echo "${grpc_get[$s]}" | awk '{print $2}')
      carga="${grpc_users[$j]}"

      if [ "$linguagem_atual" = "java" ]; then
        host="java-grpc:8082"
        protoPath="/protos/java/"
      else
        host="kotlin-grpc:8086"
        protoPath="/protos/kotlin/"
      fi

      docker run --rm \
        --user "$(id -u):$(id -g)" \
        --network docker-pratica_default \
        -v "$(pwd)/servico-musica-java/java.grpc/src/main/proto:/protos/java" \
        -v "$(pwd)/servico-musica-kotlin/kotlin.grpc/src/main/proto:/protos/kotlin" \
        -v "$(pwd)/resultados-grpc:/resultados-grpc" \
        ghcr.io/bojand/ghz:latest \
        --insecure \
        --proto "${protoPath}${proto}.proto" \
        --call "$service" \
        -d '{}' \
        -c "$carga" \
        -z 1m \
        -O json \
        -o "/resultados-grpc/${tipo_teste[$j]}/api-grpc-${linguagem_atual}/api-grpc-${linguagem_atual}_${proto}_get_u${carga}.json" \
        "$host"
      ret=$?

      echo "ta indo"
      if [ $ret -ne 0 ]; then
        echo "ERRO GET: $linguagem_atual | $service"
      fi

    done
  done
done

for a in "${!linguagem[@]}"; do
  for j in "${!tipo_teste[@]}"; do
    for s in "${!grpc_post[@]}"; do

      linguagem_atual="${linguagem[$a]}"
      service=$(echo "${grpc_post[$s]}" | awk '{print $1}')
      proto=$(echo "${grpc_post[$s]}" | awk '{print $2}')
      payload=$(echo "${grpc_post[$s]}" | cut -d' ' -f3-)
      carga="${grpc_users[$j]}"

      if [ "$linguagem_atual" = "java" ]; then
        host="java-grpc:8082"
        protoPath="/protos/java/"
      else
        host="kotlin-grpc:8086"
        protoPath="/protos/kotlin/"
      fi

      docker run --rm \
        --user "$(id -u):$(id -g)" \
        --network docker-pratica_default \
        -v "$(pwd)/servico-musica-java/java.grpc/src/main/proto:/protos/java" \
        -v "$(pwd)/servico-musica-kotlin/kotlin.grpc/src/main/proto:/protos/kotlin" \
        -v "$(pwd)/resultados-grpc:/resultados-grpc" \
        ghcr.io/bojand/ghz:latest \
        --insecure \
        --proto "${protoPath}${proto}.proto" \
        --call "$service" \
        -d "$payload" \
        -c "$carga" \
        -z 1m \
        -O json \
        -o "/resultados-grpc/${tipo_teste[$j]}/api-grpc-${linguagem_atual}/api-grpc-${linguagem_atual}_${proto}_post_u${carga}.json" \
        "$host"
      ret=$?

      if [ $ret -ne 0 ]; then
        echo "ERRO POST: $linguagem_atual | $service"
      fi

    done
  done
done