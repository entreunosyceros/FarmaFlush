# Verificador PVP

[← Índice](README.md) · [← Arquitectura](arquitectura.md) · [Parafarmacia →](parafarmacia.md) · [README del proyecto](../README.md)

---

## Verificador individual (`/verificar-precio`)

<div align="center">
<img width="993" height="1602" alt="busqueda-medicamentos" src="https://github.com/user-attachments/assets/c015a2bd-0b9e-4253-a5b4-64d855d7e57e" />
</div>

El usuario introduce medicamento y precio cobrado. El sistema:

1. Localiza el producto en el Nomenclátor SNS (**hybrid matcher**)
2. Muestra el **PVP oficial** (precio máximo intervenido)
3. Emite un veredicto:

| Nivel | Condición | Mensaje |
|-------|-----------|---------|
| ✅ OK | `\|diff\| ≤ 0,05 €` | Has pagado el precio correcto |
| ℹ️ Inferior | `diff < -0,05 €` | Pagaste menos (posible copago) |
| ⚠️ Superior | `0,05 € < diff ≤ 10%` | Pagaste más del oficial |
| 💸 Diferencia elevada | `diff > 10%` | Podrías haber pagado de más |

4. Muestra **badge de confianza** (ALTA / MEDIA / BAJA).
5. Si la confianza es `probable` (80–91) o `débil` (< 80), presenta **candidatos** para confirmar antes del veredicto.

## Modo ticket (`/verificar-ticket`)

<div align="center">
<img width="1031" height="1802" alt="verificador-ticket" src="https://github.com/user-attachments/assets/1f84a638-ddbc-4a7d-9d1d-f522bab22a73" />
</div>

Auditoría multi-producto del ticket de farmacia:

```
Ibuprofeno 600mg 20 comp.   →  3,20 €   ✅ OK
Paracetamol 1g 20 comp.     →  2,80 €   ✅ OK
Nolotil 575mg 10 cáp.       →  4,10 €   🚨 +28%
```

- Formulario dinámico (añadir/eliminar filas, HTMX)
- Resumen ejecutivo legible
- Tabla con filas explicativas en alertas
- Lenguaje factual, sin acusaciones
- **Exportar Informe de Auditoría Ciudadana (PDF):** documento formal con ID único, resumen, desfases, metodología, aviso legal y checklist (útil en mostrador o reclamaciones)

### Trazabilidad de anomalías

Permite distinguir error puntual vs patrón sistemático (p. ej. TPV desincronizado). No identifica farmacias ni atribuye intencionalidad.

## Hybrid matcher (FTS5 + rapidfuzz)

```
Texto libre → normalizar
           → FTS5 LIMIT 60
           → rapidfuzz token_set_ratio
           → bonuses: dosis (+15), unidades (+10), forma (+8), PA (+10)
           → penalty: PA ausente (−20)
           → confianza: seguro ≥92 · probable ≥80 · débil <80
```

| Confianza | Score | Comportamiento |
|-----------|-------|----------------|
| `seguro` | ≥ 92 | Veredicto directo (ALTA) |
| `probable` | 80–91 | Candidatos a confirmar (MEDIA) |
| `débil` | < 80 | Candidatos a confirmar (BAJA) |

Ejemplos probados: ibuprofeno 600mg, paracetamol 1g, nolotil 575mg, lorazepam 1mg → score 100 seguro.

## Financiación SNS (BIFIMED)

Badge en cada ficha según [BIFIMED](https://www.sanidad.gob.es/profesionales/medicamentos.do?metodo=buscarMedicamentos):

| Badge | Significado |
|-------|-------------|
| **Financiado SNS** | Cubierto por el SNS |
| **No financiado** | Fuera de financiación pública |
| **Excluido** | Retirado por resolución |

Consulta en paralelo al cargar la ficha; caché 24 h.

> **Nota:** `precio_oficial` solo viene del Nomenclátor SNS. Vademécum es referencia, nunca precio regulado.

## Detección de errores de TPV

Diseñado para detectar desincronización entre TPV y Nomenclátor. Un sobreprecio aislado puede ser error manual; un patrón en varias líneas del ticket apunta a configuración sistemática.

Marco legal del tono informativo: [Marco legal](marco-legal.md).

---

[← Índice](README.md) · [← Arquitectura](arquitectura.md) · [Parafarmacia →](parafarmacia.md) · [Frontend →](frontend.md)
