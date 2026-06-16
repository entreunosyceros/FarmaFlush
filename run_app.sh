#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_FILE="$PROJECT_DIR/app.py"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
VENV_PIP="$PROJECT_DIR/.venv/bin/pip"
PORT="5000"

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "No se encontró el entorno virtual en: $VENV_PYTHON" >&2
    echo "Creando entorno virtual en $PROJECT_DIR/.venv ..." >&2

    if ! command -v python3 >/dev/null 2>&1; then
        echo "Error: python3 no está disponible en PATH." >&2
        exit 1
    fi

    python3 -m venv "$PROJECT_DIR/.venv"

    if [[ ! -x "$VENV_PYTHON" ]]; then
        echo "Error: no se pudo crear el entorno virtual correctamente." >&2
        exit 1
    fi

    echo "Instalando dependencias..." >&2
    "$VENV_PIP" install -U pip >/dev/null
    if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
        "$VENV_PIP" install -r "$PROJECT_DIR/requirements.txt"
    else
        echo "Aviso: no existe requirements.txt; se arranca sin instalar dependencias." >&2
    fi
fi

mapfile -t project_pids < <(pgrep -f "(^|/)(python|python3|\.venv/bin/python)( .*)? $APP_FILE$|(^|/)(python|python3|\.venv/bin/python)( .*)? app\.py$" || true)

if (( ${#project_pids[@]} > 0 )); then
    echo "Cerrando instancia previa del proyecto: ${project_pids[*]}"
    kill "${project_pids[@]}" || true

    for _ in {1..20}; do
        mapfile -t remaining_pids < <(pgrep -f "(^|/)(python|python3|\.venv/bin/python)( .*)? $APP_FILE$|(^|/)(python|python3|\.venv/bin/python)( .*)? app\.py$" || true)
        if (( ${#remaining_pids[@]} == 0 )); then
            break
        fi
        sleep 0.2
    done

    if (( ${#remaining_pids[@]} > 0 )); then
        echo "Forzando cierre de procesos restantes: ${remaining_pids[*]}"
        kill -9 "${remaining_pids[@]}" || true
    fi
fi

port_pids="$(ss -ltnp 2>/dev/null | awk -v port=":$PORT" '$4 ~ port {print $NF}')"
if [[ -n "$port_pids" ]]; then
    if ss -ltnp 2>/dev/null | grep -q ":$PORT "; then
        echo "El puerto $PORT sigue ocupado por otro proceso ajeno al proyecto." >&2
        echo "Libéralo manualmente o cambia el puerto antes de continuar." >&2
        ss -ltnp | grep ":$PORT " >&2 || true
        exit 1
    fi
fi

cd "$PROJECT_DIR"
echo ""
echo "Iniciando FarmaFLUSH en http://127.0.0.1:${PORT}/ ..."
echo ""
exec "$VENV_PYTHON" "$APP_FILE"