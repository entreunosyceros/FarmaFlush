# Política de seguridad

## Versiones con soporte

| Versión | Soportada |
| ------- | --------- |
| 1.0.x   | ✅        |
| < 1.0   | ❌        |

## Alcance

Este proyecto es una aplicación web (PWA) construida con Flask y SQLite, diseñada principalmente para su ejecución en local o en servidores privados (VPS). En el ámbito de seguridad nos interesa especialmente:

- Ejecución de código o comandos no previstos (Inyecciones SQL en SQLite/FTS5 o XSS a través de componentes HTMX).
- Exposición involuntaria de datos de configuración críticos debido a un mal ajuste del archivo `.env` (como dejar `FLASK_DEBUG=1` o usar la `FLASK_SECRET_KEY` por defecto en entornos abiertos).
- Fugas de información en los logs (`busqueda_log`) que comprometan la privacidad de las consultas de los usuarios.
- Dependencias con vulnerabilidades conocidas en el ecosistema de Python que afecten al entorno de ejecución.
- Comportamientos inseguros en los scripts de automatización local (`run_app.sh` y `run_app.bat`).

**Fuera de alcance habitual:** La disponibilidad de las APIs externas (CIMA/AEMPS, Ministerios), cambios no anunciados en las estructuras web de las farmacias online que rompan los scrapers, o decisiones de salud tomadas por los usuarios basadas en los precios de referencia.

## Cómo reportar una vulnerabilidad

1. **No** abras un issue público con detalles del fallo de seguridad.
2. Usa [GitHub Security Advisories](https://github.com/entreunosyceros/FarmaFlush/security/advisories/new) (**Report a vulnerability**) si la opción está habilitada en este repositorio.
3. Si no puedes usar Advisories, abre un issue con el título `SECURITY (sin detalles)` y solicita un canal de comunicación privado; por favor, no incluyas pasos de explotación en el tablón público.

Incluye, en la medida de lo posible:
- Descripción del problema y componente afectado (ej. módulo de base de datos, servicio de un scraper concreto, etc.).
- Pasos detallados para reproducir el fallo.
- Impacto estimado (local, red, exposición del servidor).
- Versión o commit afectado.
- Sugerencia de mitigación, si dispones de ella.

## Qué esperar

- **Acuse de recibo:** Evaluación inicial en un plazo razonable de pocos días.
- **Resolución:** Parche, mitigación o refactorización del componente afectado en una versión posterior si procede.
- **Créditos:** Reconocimiento público al informante en las notas de la release, salvo que se solicite expresamente el anonimato.

## Buenas prácticas para usuarios

- **Configuración segura:** Asegúrate de cambiar la `FLASK_SECRET_KEY` en tu archivo `.env` y establecer `FLASK_DEBUG=0` si vas a exponer la aplicación en tu red local o en un VPS.
- **Privacidad:** No compartas el archivo de la base de datos `data/pildora.db` si te preocupa que otros usuarios vean el historial local de la tabla `busqueda_log`.
- **Actualizaciones:** Mantén Python y las dependencias del proyecto actualizadas ejecutando habitualmente `pip install -r requirements.txt --upgrade`.
- **Origen seguro:** Descarga el código y los releases únicamente desde el [repositorio oficial de FarmaFLUSH](https://github.com/entreunosyceros/FarmaFlush).