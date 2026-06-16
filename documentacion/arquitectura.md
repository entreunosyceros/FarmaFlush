# Arquitectura

[← Índice](README.md) · [← Inicio rápido](inicio-rapido.md) · [Verificador PVP →](verificador.md) · [README del proyecto](../README.md)

---

## Propuesta de valor

| Lo que NO hacemos | Lo que SÍ somos |
|---|---|
| ❌ Comparar y buscar "el más barato" | ✅ Verificador de precio correcto vs oficial |
| ❌ Agregador de ofertas | ✅ Referencia al PVP máximo intervenido por ley |
| ❌ Acusar a nadie | ✅ Educamos + alertamos con fuente oficial |

**Primaria:** ¿El precio cobrado coincide con el PVP oficial del Nomenclátor SNS?  
**Secundaria:** Comparativa de precios de parafarmacia en farmacias online.

## Dos capas de producto

FarmaFLUSH separa dos contextos que **no se mezclan** en la misma pantalla:

| Capa | Rutas | Fuente de verdad | Tipo de precio |
|------|-------|------------------|----------------|
| 🏛️ **Verificador** | `/verificar-precio` · `/verificar-ticket` | Nomenclátor SNS (AEMPS) | Regulado (PVP máximo intervenido) |
| 🧴 **Comparador** | `/parafarmacia` | Farmacias online (scraping) | Libre (mercado) |

**Regla de oro:** el verificador no muestra precios de farmacias online para medicamentos regulados; el comparador no usa el PVP oficial del SNS como referencia.

El puente entre capas es un enlace discreto: _"¿Buscas este producto en farmacias online? → Ver opciones de compra"_.

## Stack tecnológico

| Capa | Tecnología |
| ---- | ---------- |
| Backend | **Flask** (Python 3.10+) |
| Frontend | **HTMX** + **Pico CSS** |
| Base de datos | **SQLite** (WAL mode) |
| Matching | **FTS5** + **rapidfuzz** |
| Fuentes principales | CIMA · Nomenclátor SNS · Vademécum · BIFIMED |
| Fuentes online | Dosfarma · Tedin · Farmacias Direct · Castrofarma · Farmacia Barata · FarmaGalicia · OpenFarma · Pontevea · Gomezulla · Amazon.es |

Detalle de fuentes: [Fuentes de datos](fuentes-datos.md).

## Estructura del repositorio

```text
FarmaFLUSH/
├── app.py                  # Aplicación Flask principal
├── run_app.sh / run_app.bat
├── config.py               # Configuración desde .env
├── database.py             # SQLite + FTS5
├── services/
│   ├── matcher.py          # Hybrid matcher
│   ├── cima.py             # API CIMA (AEMPS)
│   ├── nomenclator.py      # Importador Nomenclátor SNS
│   ├── precios.py          # Agregación de precios
│   ├── informe_auditoria.py # PDF modo ticket
│   ├── vademecum.py        # Complemento informativo
│   ├── bifimed.py          # Financiación SNS
│   ├── farmacia.py         # Orquestador scrapers
│   └── farmacia_*.py       # Un scraper por fuente
├── assets/fonts/           # Fuentes DejaVu (PDF)
├── static/                 # CSS, JS, PWA, imágenes
├── templates/              # Plantillas HTMX
├── data/                   # pildora.db
└── documentacion/          # Esta documentación
```

## Base de datos — `pildora.db`

Caché local de **datos oficiales y precios scrapeados**, no una BD propietaria. Evita repetir peticiones HTTP en cada búsqueda.

### Tablas principales

| Tabla | Origen | Uso |
|-------|--------|-----|
| `nomenclator_producto` | CSV Nomenclátor SNS | Búsqueda por nombre/CN |
| `precio` (nomenclator) | CSV Nomenclátor SNS | PVP oficial del verificador |
| `medicamento` / `presentacion` | API CIMA | Fichas y relación CN ↔ nregistro |
| `precio` (otras fuentes) | Scrapers | Parafarmacia |
| `medicamento_features` | Generada | Índice del matcher (FTS5) |
| `busqueda_log` | App | «Más buscados» (7 días) |
| `importacion` | App | Auditoría de importaciones |

### Ciclo de vida

```
Primer arranque → importa Nomenclátor si precio vacío → genera medicamento_features
Búsqueda      → consulta SQLite (ms) → CIMA solo si hace falta o > 24 h
Renovación    → flask importar-nomenclator (datos mensuales)
```

### Por qué no consultar el Ministerio en cada búsqueda

El CSV tiene ~20.000 filas. Descargarlo en cada petición implicaría latencia de segundos y dependencia total del servidor externo. Con SQLite, la búsqueda responde en milisegundos.

SQLite WAL:

```python
conn.execute('PRAGMA journal_mode=WAL')
```

---

[← Índice](README.md) · [← Inicio rápido](inicio-rapido.md) · [Verificador PVP →](verificador.md) · [Fuentes de datos →](fuentes-datos.md)
