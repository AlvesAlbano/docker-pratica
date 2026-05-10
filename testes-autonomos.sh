#!/bin/bash

tipo_teste=("leve" "médio" "pesado")

tipo_servico=(
  "api-py-sem-redis"
  "api-py-redis"
  "api-ruby-sem-redis"
  "api-ruby-redis"
)

servico_url=(
  "http://api-py-sem-redis:5000"
  "http://api-py-redis:5000"
  "http://api-ruby-sem-redis:4567"
  "http://api-ruby-redis:4567"
)

u=(10 25 50)
r=(5 5 5)

# u=(150 250 350)
# r=(20 20 20)

for i in "${!tipo_teste[@]}"; do
  for j in "${!tipo_servico[@]}"; do
    docker compose run --rm locust -f teste-carga.py --request-name=${tipo_servico[$j]} --host=${servico_url[$j]} --headless -u ${u[$i]} -r ${r[$i]} -t 1m --csv=./resultados/${tipo_teste[$i]}/${tipo_servico[$j]}/${tipo_servico[$j]}_${u[$i]}_${r[$i]}

    # echo "docker compose run --rm locust -f teste-carga.py --request-name=${tipo_servico[$j]} --host=${servico_url[$j]} --headless -u ${u[$i]} -r ${r[$i]} -t 5s --csv=./resultados/${tipo_teste[$i]}/${tipo_servico[$j]}/${tipo_servico[$j]}_${u[$i]}_${r[$i]}"

  done
done