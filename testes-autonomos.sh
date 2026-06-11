#!/bin/bash

# =========================
# CONFIGURAÇÕES
# =========================

tipo_teste=("leve" "medio" "pesado")
tipo_api=("rest" "soap" "graphql")

u=(100 200 300)
r=(15 30 75)

api_url_java=(
  "http://java-rest:8080"
  "http://java-soap:8081"
  "http://java-graphql:8083"
)

# # =========================
# # JAVA LOCUST
# # =========================

for j in "${!tipo_teste[@]}"; do
  for x in "${!tipo_api[@]}"; do

    test="${tipo_teste[$j]}"
    api="${tipo_api[$x]}"
    users="${u[$j]}"
    rate="${r[$j]}"
    host="${api_url_java[$x]}"

    docker compose run --rm locust \
      -f "/mnt/locust/teste-carga-${api}-java.py" \
      --host="$host" \
      --headless \
      -u "$users" \
      -r "$rate" \
      -t 3m \
      --csv="/mnt/locust/resultados/${test}/api-${api}-java/api-${api}-java_${test}_u${users}_r${rate}"

    echo "bora krl"
  done
done

# =========================
# KOTLIN CONFIG
# =========================

api_url_kotlin=(
  "http://kotlin-rest:8084"
  "http://kotlin-soap:8085"
  "http://kotlin-graphql:8087"
)

# =========================
# KOTLIN LOCUST
# =========================

for j in "${!tipo_teste[@]}"; do
  for x in "${!tipo_api[@]}"; do

    test="${tipo_teste[$j]}"
    api="${tipo_api[$x]}"
    users="${u[$j]}"
    rate="${r[$j]}"
    host="${api_url_kotlin[$x]}"

    docker compose run --rm locust \
      -f "/mnt/locust/teste-carga-${api}-kotlin.py" \
      --host="$host" \
      --headless \
      -u "$users" \
      -r "$rate" \
      -t 3m \
      --csv="/mnt/locust/resultados/${test}/api-${api}-kotlin/api-${api}-kotlin_${test}_u${users}_r${rate}"

  done
done

# =========================
# GRPC CONFIG
# =========================

linguagem=("java" "kotlin")

# =========================
# GRPC LOCUST
# =========================

for lang in "${linguagem[@]}"; do
  for j in "${!u[@]}"; do

    usuarios="${u[$j]}"
    spawn="${r[$j]}"
    test="${tipo_teste[$j]}"
    
    # echo "FILE=$file"
    
    if [ "$lang" = "java" ]; then
      host="http://java-grpc:8082"
      csv="resultados/${test}/api-grpc-java"
      file="/mnt/locust/teste-carga-grpc-java.py"
    else
      host="http://kotlin-grpc:8086"
      csv="resultados/${test}/api-grpc-kotlin"
      file="/mnt/locust/teste-carga-grpc-kotlin.py"
    fi
    docker compose run --rm locust \
      -f "$file" \
      --host="$host" \
      --headless \
      -u "$usuarios" \
      -r "$spawn" \
      -t 3m \
      --csv="/mnt/locust/${csv}/api-grpc-${lang}_${test}_u${usuarios}_r${spawn}"

  done
done

echo
echo "Execução finalizada!"