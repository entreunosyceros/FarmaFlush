# Parafarmacia y búsqueda

[← Índice](README.md) · [← Verificador PVP](verificador.md) · [Frontend →](frontend.md) · [README del proyecto](../README.md)

---

## Búsqueda de medicamentos

- Consulta CIMA (AEMPS) + cruce con Nomenclátor SNS y Vademécum
- Filtrado por marca, forma, dosis, dispensación
- Búsqueda asíncrona con polling progresivo
- Caché 12 h por `consulta + página + tamaño`
- Resultados Nomenclátor y Vademécum en bloques separados y deduplicados

## Comparador de parafarmacia (`/parafarmacia`)

<div align="center">
<img width="1047" height="1750" alt="parafarmacia" src="https://github.com/user-attachments/assets/7c584e5d-a4de-4b0c-9617-f1609e945f6e" />
</div>

- Búsqueda paralela en múltiples fuentes
- Precio de mostrador opcional para comparar
- Transparencia: indica farmacias sin el producto
- Enlace directo a cada ficha en la farmacia
- **Ubicación** de la fuente (provincia/ciudad o `Nacional`)

| Fuente | Ubicación mostrada |
|--------|-------------------|
| Dosfarma | Murcia — Cartagena |
| Farmacia Tedin | A Coruña — Santiago de Compostela |
| Farmacias Direct | Sevilla — Sevilla |
| Castrofarma | Lugo — Castro de Rei |
| Farmacia Barata | Madrid/Almería — Madrid (Vera) |
| FarmaGalicia | Lugo — Monforte de Lemos |
| OpenFarma | Alicante — Alicante |
| Farmacia Pontevea | A Coruña — Teo (Pontevea) |
| Gomezulla | Madrid — Madrid |
| Amazon.es | Nacional |

Lista completa de fuentes: [Fuentes de datos](fuentes-datos.md).

## Filtrado de medicamentos en parafarmacia

Los scrapers pueden devolver medicamentos regulados mezclados con parafarmacia. Dos capas en `services/farmacia.py`:

1. **Regex (O(1)):** formas farmacéuticas, concentraciones, EFG/ECG (~95 % de casos).
2. **CN lookup:** si pasa la regex, consulta Nomenclátor vía matcher; si confianza `seguro` (≥ 92), se descarta. Caché `lru_cache(512)`.

## Precios diferenciados por formato

La consulta a farmacias incluye la **dosis del medicamento**, no solo el término genérico del usuario.

Prioridad de consulta:

1. INN + dosis (ej. `PARACETAMOL 650 mg`)
2. INN sin dosis
3. INN base sin sufijo de sal + dosis
4. Término original del usuario

### Marca vs principio activo

Si el usuario busca una **marca**, se intenta primero por nombre comercial. Sin resultados, **fallback** a principio activo/dosis con **aviso visible** en la UI.

## Precio de referencia vs precio de farmacia

| Situación | Mensaje |
|-----------|---------|
| Ofertas online | Precio más bajo + enlace a la farmacia |
| Solo Nomenclátor/Vademécum | Precio de referencia (sin enlace) |
| Receta sin precio | Enlace al Nomenclátor |
| Sin datos | Precio no disponible |

## Favoritos (`/favoritos`)

- Guardado en `localStorage` (solo `nregistro` + fecha)
- `POST /api/favoritos` devuelve tarjetas con datos frescos de CIMA + Nomenclátor
- Precarga silenciosa para acceso offline
- Aviso: lista informativa, no sustituye consejo médico/farmacéutico

## Circuit breaker en scrapers

- Timeout de lectura 6 s
- Tras `ReadTimeout`, pausa la fuente 60 s
- Un solo log `DEBUG` en lugar de tracebacks repetidos

---

[← Índice](README.md) · [← Verificador PVP](verificador.md) · [Frontend →](frontend.md) · [Fuentes de datos →](fuentes-datos.md)
