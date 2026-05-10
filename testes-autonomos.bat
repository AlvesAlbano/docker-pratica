@echo off
setlocal enabledelayedexpansion

:: Arrays simulados
set tipo_teste[0]=leve
set tipo_teste[1]=medio
set tipo_teste[2]=pesado

set tipo_servico[0]=api-py-sem-redis
set tipo_servico[1]=api-py-redis
set tipo_servico[2]=api-ruby-sem-redis
set tipo_servico[3]=api-ruby-redis

set servico_url[0]=http://api-py-sem-redis:5000
set servico_url[1]=http://api-py-redis:5000
set servico_url[2]=http://api-ruby-sem-redis:4567
set servico_url[3]=http://api-ruby-redis:4567

set u[0]=150
set u[1]=250
set u[2]=350

set r[0]=5
set r[1]=5
set r[2]=5

:: Loop principal
for /L %%i in (0,1,2) do (
    for /L %%j in (0,1,3) do (

        echo Executando teste !tipo_teste[%%i]! para !tipo_servico[%%j]!

        docker compose run --rm locust ^
        -f teste-carga.py ^
        --request-name=!tipo_servico[%%j]! ^
        --host=!servico_url[%%j]! ^
        --headless ^
        -u !u[%%i]! ^
        -r !r[%%i]! ^
        -t 1m ^
        --csv=./resultados/!tipo_teste[%%i]!/!tipo_servico[%%j]!/!tipo_servico[%%j]!_!u[%%i]!_!r[%%i]!

    )
)

endlocal
pause