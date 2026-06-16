# Frontend y UX

[← Índice](README.md) · [← Parafarmacia](parafarmacia.md) · [Fuentes de datos →](fuentes-datos.md) · [README del proyecto](../README.md)

---

## Separación de responsabilidades

- `templates/base.html` — layout (estructura + assets)
- `static/css/style.css` — estilos
- `static/js/app.js` — lógica cliente

CSS y JS externalizados permiten caché del navegador entre páginas.

## HTMX

- Indicador global: `hx-indicator="#global-progress"`
- Barra de progreso con texto de fase (ej. `58% · Procesando resultados…`)
- Cierre al 100 % vía evento `ff:cargaCompleta` en búsquedas progresivas
- Navegación con `sessionStorage` para transiciones entre secciones

## Rendimiento

- Inicialización bajo `DOMContentLoaded` en `app.js`
- `requestAnimationFrame` throttle en scroll (`rafThrottle`)
- Botón «Subir arriba» y cabecera compacta (`body.logo-compacto`)

## PWA

- `static/manifest.json` + `static/sw.js`
- Iconos `icon-192.png` / `icon-512.png`
- Banner de instalación en móvil:
  - Android/Chrome: `beforeinstallprompt`
  - iOS: instrucciones «Añadir a pantalla de inicio»
  - Rechazo: pausa 7 días; oculto tras `appinstalled`
- Mensaje del pie «Instálame en tu móvil…» **solo en dispositivos táctiles**
- HTTPS obligatorio en producción para instalación real

## Navegación y consistencia

- Botones Pico CSS `role="button"` en el verificador
- Quick-filters: «🧾 Verificar ticket» y «🔥 Más buscados» (separados por medicamento/parafarmacia)
- Banners cruzados medicamentos ↔ parafarmacia
- Header sticky con accesos «💊 Medicamentos» / «💄 Parafarmacia» y logo contextual
- Badge de confianza como pill (verde / amarillo / rojo)
- Candidatos del matcher como tarjetas clicables
- Páginas 404/500 personalizadas con enlaces a ambos buscadores
- Bloques premium Nomenclátor / Vademécum con contadores y pills de fuente

---

[← Índice](README.md) · [← Parafarmacia](parafarmacia.md) · [Fuentes de datos →](fuentes-datos.md) · [Marco legal →](marco-legal.md)
