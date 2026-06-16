# Inicio rápido

[← Índice](README.md) · [Arquitectura →](arquitectura.md) · [README del proyecto](../README.md)

---

## Requisitos

- **Python 3.10+**
- Navegador moderno (la app es una PWA con HTMX)

## Arranque recomendado

### Linux / macOS

```bash
git clone https://github.com/entreunosyceros/FarmaFlush.git
cd FarmaFlush
cp .env.example .env
# Edita .env: cambia FLASK_SECRET_KEY y deja FLASK_DEBUG=0
./run_app.sh
```

### Windows

```bat
git clone https://github.com/entreunosyceros/FarmaFlush.git
cd FarmaFlush
copy .env.example .env
REM Edita .env: cambia FLASK_SECRET_KEY y deja FLASK_DEBUG=0
run_app.bat
```

`run_app.bat` crea `.venv` si no existe, instala dependencias y libera el puerto 5000 si está ocupado.

La app queda en **http://127.0.0.1:5000/**

### Arranque manual

**Linux / macOS:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

**Windows:**

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

## Configuración (`.env`)

Copia `.env.example` a `.env` y ajusta estos valores **antes** de arrancar, sobre todo en producción:

| Variable | Descripción | Acción requerida |
|----------|-------------|-----------------|
| `FLASK_SECRET_KEY` | Clave para cookies de sesión Flask | **Obligatorio cambiar.** `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | Modo debug de Werkzeug | **`0` en producción.** Con `1` se expone el depurador |
| `LOG_LEVEL` | Nivel de log (`INFO`, `WARNING`, `DEBUG`…) | Por defecto `INFO`. Peticiones HTTP solo en `DEBUG` |
| `DATABASE_PATH` | Ruta SQLite | Por defecto `data/pildora.db` |
| `NOMENCLATOR_CSV_URL` | URL CSV Nomenclátor SNS | Solo si cambia la URL oficial |
| `CIMA_API_BASE` | API REST CIMA (AEMPS) | Solo si cambia el endpoint |

Ejemplo:

```env
FLASK_SECRET_KEY=tu-clave-secreta-aqui
FLASK_DEBUG=0
LOG_LEVEL=INFO
DATABASE_PATH=data/pildora.db
```

## Notas sobre la consola

Al arrancar verás `Serving Flask app` y `✅ FarmaFLUSH listo en http://127.0.0.1:5000/`. **No son errores.**

Con `LOG_LEVEL=INFO` no se imprimen las peticiones `GET / ... 200` de Werkzeug. Activa `LOG_LEVEL=DEBUG` solo para depurar.

## Primera ejecución

Si la tabla de precios del Nomenclátor está vacía, la app **importa el CSV oficial** al arrancar (~20.000 filas). Puede tardar unos minutos.

Para renovar datos más adelante: `flask importar-nomenclator` (o borra `data/pildora.db` y reinicia).

## Producción (VPS)

```bash
gunicorn app:app -b 0.0.0.0:5000 -w 2
```

Coloca un reverse proxy (nginx/Caddy) delante para HTTPS. La PWA en móvil requiere HTTPS en producción.

## Demo online

La demo en PythonAnywhere **ya no está disponible** (límites del hosting gratuito con scraping paralelo). El proyecto está pensado para **ejecución local** o en un VPS propio.

---

[← Índice](README.md) · [Arquitectura →](arquitectura.md) · [Verificador PVP](verificador.md)
