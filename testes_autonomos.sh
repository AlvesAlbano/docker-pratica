#!/bin/bash

classe=("leve" "medio" "pesado")
instancias=(1 2 3)
postagem=("post_texto_400kb" "post_imagem_1mb" "post_imagem_300kb" "todos")
arquivo_py=("teste-carga-texto-400kb" "teste-carga-imagem-1mb" "teste-carga-imagem-300kb" "teste-carga-todos")

u=(150 300 1500)
r=(12 12 12)

for i in "${!classe[@]}"; do
  for j in "${!instancias[@]}"; do
    cp "nginx/nginx-${instancias[$j]}.conf" "nginx/nginx.conf"
    docker exec nginx nginx -s reload

    for x in "${!postagem[@]}"; do
      echo "Classe: ${classe[$i]} | Instancia: ${instancias[$j]} | Teste: ${postagem[$x]}"
      docker compose run --rm locust \
        -f "${arquivo_py[$x]}.py" \
        --host=http://nginx \
        --headless \
        -u "${u[$i]}" \
        -r "${r[$i]}" \
        -t 1m \
        --csv="./resultados/${classe[$i]}/instancia_${instancias[$j]}/${postagem[$x]}/${postagem[$x]}_${u[$i]}_usuarios"

    done
  done
done