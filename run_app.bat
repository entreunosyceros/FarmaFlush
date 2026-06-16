@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ------------------------------------------------------------
REM FarmaFlush - Windows launcher (BAT)
REM - Stops previous app.py processes (best-effort)
REM - Frees port 5000 if occupied (best-effort)
REM - Ensures .venv exists
REM - Installs requirements.txt
REM - Runs app.py
REM ------------------------------------------------------------

set "PROJECT_DIR=%~dp0"
set "APP_FILE=%PROJECT_DIR%app.py"
set "VENV_PY=%PROJECT_DIR%.venv\Scripts\python.exe"
set "VENV_PIP=%PROJECT_DIR%.venv\Scripts\pip.exe"
set "PORT=5000"

pushd "%PROJECT_DIR%" >nul

if not exist "%APP_FILE%" (
  echo Error: No se encontro app.py en: "%APP_FILE%"
  popd >nul
  exit /b 1
)

REM --- Cerrar instancias previas (por comando app.py) ---
REM Usamos PowerShell para localizar por CommandLine y matar.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p='%APP_FILE%'.Replace('\','\\');" ^
  "$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match [regex]::Escape($p) };" ^
  "if ($procs) { $ids = $procs.ProcessId -join ','; Write-Host ('Cerrando instancias previas de app.py: ' + $ids); $procs | ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop } catch {} } }"

REM --- Liberar puerto si esta ocupado ---
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$port=%PORT%;" ^
  "$conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue;" ^
  "if ($conns) { $pids = $conns.OwningProcess | Select-Object -Unique; Write-Host ('Liberando puerto ' + $port + ' (PID): ' + ($pids -join ',')); $pids | ForEach-Object { try { Stop-Process -Id $_ -Force -ErrorAction Stop } catch {} } }"

REM --- Crear venv si no existe ---
if not exist "%VENV_PY%" (
  echo No se encontro el entorno virtual en: "%VENV_PY%"
  echo Creando entorno virtual en "%PROJECT_DIR%.venv"...

  where python >nul 2>&1
  if errorlevel 1 (
    echo Error: Python no esta disponible en PATH. Instala Python 3 y reinicia la consola.
    popd >nul
    exit /b 1
  )

  python -m venv ".venv"
  if errorlevel 1 (
    echo Error: no se pudo crear el entorno virtual.
    popd >nul
    exit /b 1
  )
)

echo Actualizando pip...
"%VENV_PY%" -m pip install -U pip
if errorlevel 1 (
  echo Error: fallo actualizando pip.
  popd >nul
  exit /b 1
)

if exist "%PROJECT_DIR%requirements.txt" (
  echo Instalando dependencias (requirements.txt)...
  "%VENV_PIP%" install -r "%PROJECT_DIR%requirements.txt"
  if errorlevel 1 (
    echo Error: fallo instalando dependencias.
    popd >nul
    exit /b 1
  )
) else (
  echo Aviso: no existe requirements.txt; se arranca sin instalar dependencias.
)

echo.
echo Iniciando aplicacion en http://127.0.0.1:%PORT% ...
echo.

"%VENV_PY%" "%APP_FILE%"
set "EXITCODE=%ERRORLEVEL%"

popd >nul
exit /b %EXITCODE%

