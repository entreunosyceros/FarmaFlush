# Fuentes de datos

[← Índice](README.md) · [← Frontend](frontend.md) · [Marco legal →](marco-legal.md) · [README del proyecto](../README.md)

---

## Fuentes oficiales

| Fuente | Tipo | Qué se obtiene |
|--------|------|----------------|
| **CIMA** (AEMPS) | API REST pública | Nombre, laboratorio, forma, dosis, ficha, prospecto, fotos |
| **Nomenclátor SNS** | Archivo oficial (sanidad.gob.es) | PVP máximo intervenido (base del verificador) |
| **Vademécum** | Consulta pública | Indicaciones, contraindicaciones, PVP de referencia |
| **BIFIMED** | Formulario Ministerio | Situación de financiación SNS |

## Farmacias online integradas

| Farmacia | Plataforma | Qué se obtiene |
|----------|-----------|----------------|
| **Dosfarma** | Algolia | Parafarmacia, vitaminas |
| **Farmacia Tedin** | Prestashop | Parafarmacia, OTC |
| **Farmacias Direct** | Shopify | OTC + parafarmacia |
| **Castrofarma** | Magento 2 | Parafarmacia, cosmética |
| **Farmacia Barata** | Prestashop | Parafarmacia |
| **FarmaGalicia** | Magento 2 | Parafarmacia |
| **OpenFarma** | Prestashop 1.6 | Parafarmacia, higiene |
| **Farmacia Pontevea** | Prestashop | Dermocosmética |
| **Gomezulla** | Prestashop | Cosmética dermatológica |
| **Amazon.es** | Marketplace | Parafarmacia (múltiples vendedores) |

> **Farmacias Direct** es la única fuente integrada que vende medicamentos OTC. El resto aportan parafarmacia.

## Exclusión voluntaria (opt-out)

Respetamos la voluntad de los comercios indexados. Titulares: [Titulares de farmacias](titulares-farmacias.md).

## Farmacias exploradas pero no integradas

| Farmacia | Razón |
|----------|-------|
| Mifarma (atida.com) | WAF + captcha → 403 |
| Promofarma | Solo parafarmacia, sin OTC |
| Labandeira | SearchAPI no configurada |
| Farmacia Toca | DNS no resuelve |
| Farmacia Loureiro | DNS no resuelve |
| Farmacia San Mamed | Cloudflare anti-bot |
| Farmacia del Camino | Sin endpoint de búsqueda |

---

[← Índice](README.md) · [← Arquitectura](arquitectura.md) · [Marco legal →](marco-legal.md) · [Titulares de farmacias →](titulares-farmacias.md)
