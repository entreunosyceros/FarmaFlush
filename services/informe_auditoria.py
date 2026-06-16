"""Generación del Informe de Auditoría Ciudadana (PDF) para el modo ticket."""

from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

from fpdf import FPDF

from config import BASE_DIR

# Paleta alineada con la UI (azul Nomenclátor)
_COLOR_TITULO = (13, 71, 161)
_COLOR_SUBTITULO = (55, 65, 81)
_COLOR_BORDE = (209, 213, 219)
_COLOR_MUTED = (107, 114, 128)

_FONT_REGULAR = "FarmaDejaVu"
_FONT_BOLD = "FarmaDejaVuBold"
_FONT_ITALIC = "FarmaDejaVuItalic"


def _resolver_fuente_dejavu() -> Path:
    candidatos = [
        BASE_DIR / "assets" / "fonts" / "DejaVuSans.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
        Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    ]
    for ruta in candidatos:
        if ruta.is_file():
            return ruta
    raise FileNotFoundError(
        "No se encontró DejaVuSans.ttf. Ejecute run_app.sh o copie la fuente a assets/fonts/."
    )


def _fmt_eur(val: float | None) -> str:
    if val is None:
        return "—"
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def _generar_id_informe(fecha: datetime) -> str:
    sufijo = secrets.token_hex(2).upper()
    return fecha.strftime(f"FF-%Y%m%d-%H%M-{sufijo}")


def _nivel_etiqueta(nivel: str) -> str:
    return {
        "ok": "Correcto",
        "inferior": "Inferior al oficial",
        "superior": "Superior al oficial",
        "excesivo": "Diferencia elevada",
    }.get(nivel, nivel)


class _InformePDF(FPDF):
    def __init__(self, informe_id: str) -> None:
        super().__init__()
        self._informe_id = informe_id
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 18, 18)
        self._registrar_fuentes()

    def _registrar_fuentes(self) -> None:
        base = _resolver_fuente_dejavu()
        bold = base.with_name("DejaVuSans-Bold.ttf")
        italic = base.with_name("DejaVuSans-Oblique.ttf")
        if not bold.is_file():
            bold = base
        if not italic.is_file():
            italic = base
        self.add_font(_FONT_REGULAR, "", str(base))
        self.add_font(_FONT_BOLD, "B", str(bold))
        self.add_font(_FONT_ITALIC, "I", str(italic))

    def _set_body(self, size: int = 9, style: str = "") -> None:
        if style == "B":
            self.set_font(_FONT_BOLD, "B", size)
        elif style == "I":
            self.set_font(_FONT_ITALIC, "I", size)
        else:
            self.set_font(_FONT_REGULAR, "", size)

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self._set_body(8, "I")
        self.set_text_color(*_COLOR_MUTED)
        self.cell(0, 6, f"FarmaFLUSH — Informe de verificación · {self._informe_id}", align="L")
        self.ln(8)

    def footer(self) -> None:
        self.set_y(-12)
        self._set_body(8, "I")
        self.set_text_color(*_COLOR_MUTED)
        self.cell(0, 8, f"Página {self.page_no()}/{{nb}} · {self._informe_id}", align="C")

    def titulo_seccion(self, texto: str) -> None:
        self.ln(4)
        self._set_body(11, "B")
        self.set_text_color(*_COLOR_TITULO)
        self.multi_cell(0, 6, texto)
        self.ln(2)
        self.set_draw_color(*_COLOR_BORDE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def parrafo(self, texto: str, size: int = 9, style: str = "") -> None:
        self._set_body(size, style)
        self.set_text_color(*_COLOR_SUBTITULO)
        self.multi_cell(0, 4.5, texto)
        self.ln(2)

    def tabla_cabecera(self, columnas: list[tuple[str, float]]) -> None:
        self._set_body(8, "B")
        self.set_fill_color(227, 242, 253)
        self.set_text_color(*_COLOR_TITULO)
        self.set_draw_color(*_COLOR_BORDE)
        for titulo, ancho in columnas:
            self.cell(ancho, 7, titulo, border=1, align="C", fill=True)
        self.ln()

    def tabla_fila(self, valores: list[str], anchos: list[float], *, bold: bool = False) -> None:
        self._set_body(8, "B" if bold else "")
        self.set_text_color(*_COLOR_SUBTITULO)
        altura = 6
        for valor, ancho in zip(valores, anchos):
            self.cell(ancho, altura, valor[:80], border=1)
        self.ln()


def generar_informe_pdf(items: list[dict[str, Any]], resumen: dict[str, Any]) -> bytes:
    """Genera el PDF del Informe de Auditoría Ciudadana y devuelve los bytes."""
    ahora = datetime.now()
    informe_id = _generar_id_informe(ahora)
    pdf = _InformePDF(informe_id)
    pdf.alias_nb_pages()
    pdf.add_page()

    # ── Cabecera ─────────────────────────────────────────────────────
    pdf._set_body(14, "B")
    pdf.set_text_color(*_COLOR_TITULO)
    pdf.multi_cell(0, 7, "INFORME DE VERIFICACIÓN DE PRECIOS (PVP OFICIAL) — FARMAFLUSH")
    pdf.ln(2)

    pdf._set_body(9)
    pdf.set_text_color(*_COLOR_SUBTITULO)
    pdf.multi_cell(
        0,
        5,
        f"Fecha y hora de generación: {ahora.strftime('%d/%m/%Y %H:%M')}\n"
        f"ID de informe: {informe_id}\n"
        "Ámbito: Nomenclátor del Sistema Nacional de Salud (Ministerio de Sanidad)\n"
        "Nota de privacidad: este informe no incluye datos personales ni identifica establecimientos.",
    )
    pdf.ln(4)

    # ── Resumen ejecutivo ────────────────────────────────────────────
    superior_leve = resumen.get("alertas", 0) - resumen.get("excesivos", 0)
    pdf.titulo_seccion("RESUMEN EJECUTIVO")
    pdf.parrafo(
        f"En esta auditoría se han verificado {resumen['total']} líneas introducidas por el usuario. "
        f"El sistema ha detectado: {resumen.get('ok', 0)} correctas · "
        f"{superior_leve} con diferencia moderada · "
        f"{resumen.get('excesivos', 0)} con diferencia elevada · "
        f"{resumen.get('inferior', 0)} por debajo del PVP oficial · "
        f"{resumen.get('sin_datos', 0)} sin PVP oficial disponible."
    )

    pdf._set_body(9, "B")
    pdf.set_text_color(*_COLOR_SUBTITULO)
    pdf.cell(0, 5, "Impacto económico estimado", ln=True)
    pdf._set_body(9)
    pdf.multi_cell(
        0,
        4.5,
        f"- Sobreprecio acumulado detectado: {_fmt_eur(resumen.get('total_sobreprecio', 0))} "
        "(suma de diferencias positivas)\n"
        f"- Ahorro acumulado detectado: {_fmt_eur(resumen.get('total_ahorro', 0))} "
        "(suma de diferencias negativas, en valor absoluto)",
    )
    pdf.ln(2)

    if resumen.get("peor_q"):
        pdf.parrafo(
            f"Mayor diferencia detectada: {resumen['peor_q']} "
            f"(+{_fmt_eur(resumen.get('peor_diff'))}"
            f"{f', {resumen['peor_pct']}%' if resumen.get('peor_pct') is not None else ''})."
        )

    pdf.parrafo(
        "Este informe compara el precio introducido con el PVP oficial del Nomenclátor SNS "
        "cuando está disponible. Si existen discrepancias, se recomienda verificar CN, dosis "
        "y unidades antes de solicitar una revisión en mostrador o adjuntar el informe a una reclamación."
    )

    # ── Desfases detectados ──────────────────────────────────────────
    desfases = [
        i for i in items
        if i.get("diferencia") and i["diferencia"]["nivel"] in ("superior", "excesivo")
    ]
    pdf.titulo_seccion("DESFASES DETECTADOS (PVP OFICIAL vs PRECIO INTRODUCIDO)")

    if desfases:
        cols = [
            ("Producto", 52),
            ("CN", 18),
            ("Cobrado", 22),
            ("PVP oficial", 22),
            ("Dif. €", 18),
            ("Dif. %", 16),
            ("Clasif.", 32),
        ]
        anchos = [c[1] for c in cols]
        pdf.tabla_cabecera(cols)
        for item in desfases:
            m = item.get("match") or {}
            d = item["diferencia"]
            nombre = m.get("nombre") or item.get("q", "")
            cn = m.get("cn") or "—"
            clasif = _nivel_etiqueta(d["nivel"])
            pct = f"+{d['pct']}%" if d.get("pct") is not None else "—"
            diff_str = f"+{_fmt_eur(d['diff'])}" if d["diff"] > 0 else _fmt_eur(d["diff"])
            pdf.tabla_fila(
                [
                    nombre,
                    str(cn),
                    _fmt_eur(item.get("precio_cobrado")),
                    _fmt_eur(d.get("pvp_oficial")),
                    diff_str,
                    pct,
                    clasif,
                ],
                anchos,
            )
    else:
        pdf.parrafo("No se han detectado desfases relevantes respecto al PVP oficial.")

    # ── Anexo: líneas sin desfase ────────────────────────────────────
    sin_desfase = [
        i for i in items
        if i.get("diferencia") and i["diferencia"]["nivel"] in ("ok", "inferior")
    ]
    sin_datos = [i for i in items if not i.get("diferencia")]

    pdf.titulo_seccion("LÍNEAS VERIFICADAS SIN DESFASE RELEVANTE (Anexo)")

    if sin_desfase or sin_datos:
        cols = [("Introducido", 48), ("Encontrado", 52), ("PVP oficial", 24), ("Cobrado", 24), ("Estado", 32)]
        anchos = [c[1] for c in cols]
        pdf.tabla_cabecera(cols)
        for item in sin_desfase + sin_datos:
            m = item.get("match") or {}
            d = item.get("diferencia")
            if d:
                estado = _nivel_etiqueta(d["nivel"])
                if d["nivel"] == "inferior":
                    estado = f"−{_fmt_eur(abs(d['diff']))}"
            else:
                estado = "Sin datos"
            pdf.tabla_fila(
                [
                    item.get("q", ""),
                    m.get("nombre") or "—",
                    _fmt_eur(m.get("pvp")) if m.get("pvp") else "—",
                    _fmt_eur(item.get("precio_cobrado")),
                    estado,
                ],
                anchos,
            )
    else:
        pdf.parrafo("Todas las líneas presentan desfase respecto al PVP oficial.")

    # ── Metodología ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.titulo_seccion("METODOLOGÍA Y FUENTES")
    pdf.parrafo(
        "Qué verifica este informe\n"
        "Este documento compara el precio introducido por el usuario con el PVP máximo oficial "
        "publicado en el Nomenclátor del Sistema Nacional de Salud (SNS) para cada medicamento identificado."
    )
    pdf.parrafo(
        "Cómo se calcula la diferencia\n"
        "Para cada línea verificada: Diferencia (€) = Precio cobrado − PVP oficial (SNS). "
        "Cuando procede: Diferencia (%) = Diferencia (€) / PVP oficial (SNS) × 100. "
        "Se aplica una tolerancia de 0,05 € para cubrir posibles redondeos."
    )
    pdf.parrafo(
        "Identificación del medicamento\n"
        "La identificación se realiza a partir del texto introducido por el usuario y/o el Código Nacional (CN) "
        "cuando está disponible. En caso de duda, pueden existir presentaciones con nombres similares; "
        "por ello se recomienda contrastar CN, dosis y número de unidades."
    )
    pdf.parrafo(
        "Fuentes utilizadas\n"
        "- Nomenclátor SNS (Ministerio de Sanidad): fuente de referencia para el PVP máximo oficial.\n"
        "- AEMPS (CIMA): fuente complementaria para ficha del medicamento, presentaciones y códigos.\n"
        "Enlaces: https://www.sanidad.gob.es/profesionales/nomenclator.do · https://cima.aemps.es"
    )

    # ── Aviso legal ──────────────────────────────────────────────────
    pdf.titulo_seccion("AVISO LEGAL Y LIMITACIONES")
    pdf.parrafo(
        "Este informe tiene carácter informativo. FarmaFLUSH no identifica establecimientos ni atribuye "
        "intencionalidad. Los datos se basan en fuentes oficiales y en la información introducida por el usuario. "
        "Si existen discrepancias, se recomienda verificar CN, dosis, formato y número de unidades antes de "
        "solicitar una revisión en mostrador o iniciar una reclamación. "
        "No constituye asesoramiento legal ni farmacéutico."
    )

    # ── Checklist ────────────────────────────────────────────────────
    pdf.titulo_seccion("CHECKLIST DE VERIFICACIÓN (ANTES DE RECLAMAR)")
    checklist = [
        "El medicamento corresponde a la misma presentación (CN, dosis y unidades).",
        "No hay confusión entre marca y genérico (EFG).",
        "El precio introducido corresponde solo a esa línea (sin productos adicionales).",
        "El PVP oficial consultado coincide con la fecha de generación de este informe.",
    ]
    pdf._set_body(9)
    pdf.set_text_color(*_COLOR_SUBTITULO)
    for punto in checklist:
        pdf.cell(5, 5, "•")
        pdf.multi_cell(0, 5, punto)
        pdf.ln(1)

    return bytes(pdf.output())
