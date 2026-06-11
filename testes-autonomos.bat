@echo off
setlocal enabledelayedexpansion

REM =========================
REM CONFIGURAÇÕES
REM =========================

set tipo_teste[0]=leve
set tipo_teste[1]=medio
set tipo_teste[2]=pesado

set tipo_api[0]=rest
set tipo_api[1]=soap
set tipo_api[2]=graphql

set u[0]=100
set u[1]=200
set u[2]=300

set r[0]=15
set r[1]=30
set r[2]=75

set api_url_java[0]=http://java-rest:8080
set api_url_java[1]=http://java-soap:8081
set api_url_java[2]=http://java-graphql:8083

REM =========================
REM JAVA LOCUST
REM =========================

for /L %%j in (0,1,2) do (
  for /L %%x in (0,1,2) do (

    set test=!tipo_teste[%%j]!
    set api=!tipo_api[%%x]!
    set users=!u[%%j]!
    set rate=!r[%%j]!
    set host=!api_url_java[%%x]!

    docker compose run --rm locust -f teste-carga-!api!-java.py ^
      --host="!host!" ^
      --headless ^
      -u !users! ^
      -r !rate! ^
      -t 4s ^
      --csv=./resultados/!test!/api-!api!-java/api-!api!-java_!test!_u!users!_r!rate!

  )
)

REM =========================
REM KOTLIN CONFIG
REM =========================

set api_url_kotlin[0]=http://kotlin-rest:8084
set api_url_kotlin[1]=http://kotlin-soap:8085
set api_url_kotlin[2]=http://kotlin-graphql:8087

REM =========================
REM KOTLIN LOCUST
REM =========================

for /L %%j in (0,1,2) do (
  for /L %%x in (0,1,2) do (

    set test=!tipo_teste[%%j]!
    set api=!tipo_api[%%x]!
    set users=!u[%%j]!
    set rate=!r[%%j]!
    set host=!api_url_kotlin[%%x]!

    docker compose run --rm locust -f teste-carga-!api!-kotlin.py ^
      --host="!host!" ^
      --headless ^
      -u !users! ^
      -r !rate! ^
      -t 4s ^
      --csv=./resultados/!test!/api-!api!-kotlin/api-!api!-kotlin_!test!_u!users!_r!rate!

  )
)

REM =========================
REM GRPC CONFIG
REM =========================

set linguagem[0]=java
set linguagem[1]=kotlin

set grpc_users[0]=100
set grpc_users[1]=200
set grpc_users[2]=300

REM =========================
REM GRPC LOCUST
REM =========================

for /L %%a in (0,1,1) do (
  for /L %%j in (0,1,2) do (

    set lang=!linguagem[%%a]!
    set carga=!grpc_users[%%j]!
    set test=!tipo_teste[%%j]!

    if "!lang!"=="java" (
      set host=http://java-grpc:8082
      set csv=./resultados/!test!/api-grpc-java
      set file=teste-carga-grpc-java.py
    ) else (
      set host=http://kotlin-grpc:8086
      set csv=./resultados/!test!/api-grpc-kotlin
      set file=teste-carga-grpc-kotlin.py
    )

    docker compose run --rm locust ^
      -f !file! ^
      --host="!host!" ^
      --headless ^
      -u !carga! ^
      -r !carga! ^
      -t 4s ^
      --csv=!csv!/api-grpc-!lang!_!test!_u!carga!_r!carga!

  )
)

echo.
echo Execucao finalizada!
pause