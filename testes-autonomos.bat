@echo off
setlocal enabledelayedexpansion

set TEMPO=2m
set HOST=http://nginx

echo Iniciando bateria de 36 testes...

call :rodar_instancia 1
call :rodar_instancia 2
call :rodar_instancia 3

echo.
echo Todos os 36 testes foram finalizados.
pause
exit /b


:rodar_instancia
set INSTANCIA=%1

echo.
echo ==========================================
echo Configurando Nginx para %INSTANCIA% instancia(s)
echo ==========================================

copy /Y nginx\nginx-%INSTANCIA%.conf nginx\nginx.conf

docker restart nginx

echo Aguardando Nginx reiniciar...
timeout /t 8 /nobreak

call :rodar_carga leve 150 20 %INSTANCIA%
call :rodar_carga medio 250 20 %INSTANCIA%
call :rodar_carga pesado 350 20 %INSTANCIA%

exit /b


:rodar_carga
set CARGA=%1
set USUARIOS=%2
set SPAWN=%3
set INSTANCIA=%4

call :rodar_teste %CARGA% %INSTANCIA% post_texto_400kb teste-carga-texto-400kb.py %USUARIOS% %SPAWN%
call :rodar_teste %CARGA% %INSTANCIA% post_imagem_1mb teste-carga-imagem-1mb.py %USUARIOS% %SPAWN%
call :rodar_teste %CARGA% %INSTANCIA% post_imagem_300kb teste-carga-imagem-300kb.py %USUARIOS% %SPAWN%
call :rodar_teste %CARGA% %INSTANCIA% todos teste-carga-todos.py %USUARIOS% %SPAWN%

exit /b


:rodar_teste
set CARGA=%1
set INSTANCIA=%2
set CENARIO=%3
set ARQUIVO=%4
set USUARIOS=%5
set SPAWN=%6

echo.
echo ------------------------------------------
echo Classe: %CARGA% ^| Instancia: %INSTANCIA% ^| Teste: %CENARIO%
echo Usuarios: %USUARIOS% ^| Spawn: %SPAWN% ^| Tempo: %TEMPO%
echo ------------------------------------------

if not exist locust\resultados\%CARGA%\instancia_%INSTANCIA%\%CENARIO% (
  mkdir locust\resultados\%CARGA%\instancia_%INSTANCIA%\%CENARIO%
)

docker compose run --rm locust ^
  -f %ARQUIVO% ^
  --host=%HOST% ^
  --headless ^
  -u %USUARIOS% ^
  -r %SPAWN% ^
  -t %TEMPO% ^
  --csv=/mnt/locust/resultados/%CARGA%/instancia_%INSTANCIA%/%CENARIO%/%CENARIO%_%USUARIOS%_usuarios

exit /b