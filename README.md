# 💊 FarmaFLUSH — Verificador de precio de medicamentos en España

<div align="center">
  <img width="350" height="350" alt="farmaflush" src="https://github.com/user-attachments/assets/c266f33a-1fab-43c4-aa97-a51188430f6f" />

  <br />

  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
  ![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
  ![Framework: Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
  [![Documentation](https://img.shields.io/badge/Documentation-Wiki-blue)](documentacion/README.md)
</div>

Verificador de precios de medicamentos (**PVP oficial del Nomenclátor SNS**) y comparador de **parafarmacia** en farmacias online.

FarmaFLUSH es una PWA que contrasta en segundos si lo cobrado en farmacia coincide con el precio máximo regulado por el Ministerio de Sanidad. También permite comparar productos de parafarmacia en varias tiendas online.

---

## ¿Qué hace?

| Lo que NO hacemos | Lo que SÍ somos |
|---|---|
| ❌ Buscar "el más barato" | ✅ Verificar precio vs PVP oficial |
| ❌ Agregador de ofertas | ✅ Referencia al precio intervenido por ley |
| ❌ Acusar a nadie | ✅ Informar con fuentes oficiales |

- **Verificador** (`/verificar-precio`, `/verificar-ticket`) — Nomenclátor SNS
- **Comparador** (`/parafarmacia`) — precios de mercado en farmacias online

---

## Arranque rápido

Clona el repositorio y crea `.env` a partir de `.env.example` (cambia `FLASK_SECRET_KEY`).

### Linux / macOS

```bash
git clone https://github.com/entreunosyceros/FarmaFlush.git
cd FarmaFlush
cp .env.example .env
./run_app.sh
```

### Windows

En **CMD** o **PowerShell**, desde la carpeta del proyecto:

```bat
git clone https://github.com/entreunosyceros/FarmaFlush.git
cd FarmaFlush
copy .env.example .env
run_app.bat
```

`run_app.bat` crea `.venv` si no existe, instala dependencias, libera el puerto 5000 si está ocupado y arranca la app.

Abre **http://127.0.0.1:5000/** en el navegador.

Detalle de instalación, `.env` y producción: **[Inicio rápido](documentacion/inicio-rapido.md)**

---

## Documentación

Toda la documentación está en la carpeta **[`documentacion/`](documentacion/README.md)**:

| Guía | Descripción |
|------|-------------|
| [📖 Índice completo](documentacion/README.md) | Mapa de toda la documentación |
| [🚀 Inicio rápido](documentacion/inicio-rapido.md) | Instalación y configuración |
| [🏗️ Arquitectura](documentacion/arquitectura.md) | Stack, estructura y base de datos |
| [🏛️ Verificador PVP](documentacion/verificador.md) | Modo ticket, PDF, matcher |
| [🧴 Parafarmacia](documentacion/parafarmacia.md) | Comparador, favoritos, filtros |
| [🎨 Frontend y UX](documentacion/frontend.md) | HTMX, PWA, navegación |
| [📊 Fuentes de datos](documentacion/fuentes-datos.md) | CIMA, scrapers, opt-out |
| [⚖️ Marco legal](documentacion/marco-legal.md) | Disclaimers y licencia |
| [🗺️ Roadmap](documentacion/roadmap.md) | Hecho y pendiente |

## Comunidad

- [Contribuir](CONTRIBUTING.md)
- [Código de conducta](CODE_OF_CONDUCT.md)
- [Seguridad](SECURITY.md)
- [Titulares de farmacias — exclusión](documentacion/titulares-farmacias.md)

---

## Licencia

MIT — ver [LICENSE](LICENSE). Proyecto informativo y educativo; no constituye asesoramiento legal ni farmacéutico.

**Repositorio:** [github.com/entreunosyceros/FarmaFlush](https://github.com/entreunosyceros/FarmaFlush)
