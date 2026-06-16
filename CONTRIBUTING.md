# Guía de contribución

¡Gracias por interesarte en **FarmaFLUSH**! Este proyecto es software libre (MIT) para verificar precios de medicamentos frente al PVP oficial del Nomenclátor SNS y comparar productos de parafarmacia en farmacias online. Cualquier mejora bien planteada es bienvenida.

## Antes de empezar

- Lee el [README](README.md) y la [documentación](documentacion/README.md) para entender las dos capas del producto: **verificador** (precio regulado) y **comparador** (mercado libre).
- Revisa las [issues abiertas](https://github.com/entreunosyceros/FarmaFlush/issues) por si alguien ya trabaja en lo mismo.
- Consulta el [Código de conducta](CODE_OF_CONDUCT.md) para el comportamiento esperado en la comunidad.
- Para vulnerabilidades, sigue [SECURITY.md](SECURITY.md) (no abras issues públicas con detalles de explotación).

## Cómo puedes ayudar

- **Reportar errores** en búsqueda, verificador, modo ticket, scrapers o exportación PDF.
- **Proponer mejoras** explicando el problema del usuario y el impacto esperado.
- **Enviar pull requests** acotados, probados y documentados cuando proceda.
- **Mejorar documentación** (README, comentarios, textos de la interfaz).
- **Corregir scrapers** cuando una farmacia online cambie su HTML o API pública.
- **Afinar el hybrid matcher** (FTS5 + rapidfuzz) si detectas falsos positivos o negativos.

## Entorno de desarrollo

Requisitos: **Python 3.10+** y navegador moderno.

```bash
git clone https://github.com/entreunosyceros/FarmaFlush.git
cd FarmaFlush
cp .env.example .env
# Edita .env: cambia FLASK_SECRET_KEY y deja FLASK_DEBUG=0
./run_app.sh
```

En Windows:

```bat
run_app.bat
```

La app queda disponible en `http://127.0.0.1:5000/`.

### Arranque manual (opcional)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Primera ejecución

En el primer arranque puede importarse el **Nomenclátor SNS** si la base de datos está vacía. Esto puede tardar unos minutos. La BD local por defecto es `data/pildora.db`.

## Áreas del código

| Área | Ubicación habitual |
|------|-------------------|
| Rutas Flask / verificador | `app.py` |
| Matcher híbrido | `services/matcher.py` |
| Nomenclátor / precios oficiales | `services/nomenclator.py`, `services/precios.py` |
| CIMA (AEMPS) | `services/cima.py` |
| Vademécum | `services/vademecum.py` |
| Scrapers parafarmacia | `services/farmacia_*.py`, `services/farmacia.py` |
| Informe PDF (modo ticket) | `services/informe_auditoria.py` |
| Plantillas HTMX | `templates/` |
| Estilos | `static/css/style.css` |

## Estilo de código

- Sigue el estilo del código existente (nombres, imports, nivel de comentarios).
- Cambios **mínimos y enfocados**: no mezcles varias funcionalidades en un mismo PR.
- Los textos visibles para el usuario van en **español**, con tono **informativo y factual** (el proyecto no acusa ni identifica establecimientos).
- No incluyas secretos (`.env`, claves API), rutas personales ni datos de tickets reales en commits o issues.
- Respeta la **regla de oro** del README: no mezclar en la misma pantalla el PVP oficial del SNS con precios de mercado de parafarmacia.

## Pull requests

1. Crea una rama descriptiva desde `main` (por ejemplo `fix/scraper-dosfarma` o `feat/ticket-pdf-qr`).
2. Describe **qué** cambias y **por qué**.
3. Indica cómo lo has probado (pasos manuales, capturas o comandos).
4. Si tocas scrapers, indica qué farmacia y qué URL o producto de prueba usaste.
5. Si tocas verificador o matcher, indica medicamento/CN de ejemplo y resultado esperado vs obtenido.
6. Actualiza el README solo si el cambio lo requiere.

Usa la [plantilla de pull request](.github/pull_request_template.md) al abrir el PR.

## Reportar problemas

- **Bugs y mejoras:** usa las plantillas de [GitHub Issues](https://github.com/entreunosyceros/FarmaFlush/issues/new/choose).
- **Solicitud de exclusión (titulares de farmacia):** plantilla «Solicitud de exclusión» o issue con título `Solicitud de Exclusión - [Nombre de la Farmacia]`.
- **Seguridad:** [SECURITY.md](SECURITY.md).

## Licencia

Al contribuir, aceptas que tu aportación se publique bajo la misma licencia del proyecto: [MIT](LICENSE).
