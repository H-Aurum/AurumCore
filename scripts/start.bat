@echo off
title AurumCore - IA para Streamers
echo Starting AurumCore...

:: Ativar ambiente virtual
call aurum-env\Scripts\activate

:: Iniciar aplicação
python -m aurumcore.core

:: Manter console aberto após encerramento
echo.
echo AurumCore foi encerrado.
echo Pressione qualquer tecla para fechar...
pause >nul
