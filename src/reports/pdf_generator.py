# src/reports/pdf_generator.py
"""
Generador de reportes PDF institucionales con ReportLab.
Diseño basado en el reporte de percepción institucional de la EMI.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image
)


# =========================================================
# PALETA DE COLORES INSTITUCIONAL
# =========================================================
COLOR_AZUL_MARINO = HexColor("#003366")
COLOR_AZUL_OSCURO = HexColor("#002244")
COLOR_AZUL_MEDIO = HexColor("#035AA6")
COLOR_GRIS_FONDO = HexColor("#F8F9FA")
COLOR_GRIS_BORDE = HexColor("#E0E4EA")
COLOR_GRIS_TEXTO = HexColor("#666666")
COLOR_TEXTO = HexColor("#2C3E50")
COLOR_VERDE = HexColor("#28A745")
COLOR_ROJO = HexColor("#DC3545")
COLOR_AMARILLO = HexColor("#F2B705")
COLOR_AZUL_CLARO = HexColor("#E8F1F9")


class ReportePDF:
    """Generador de reportes institucionales en PDF."""

    def __init__(self, output_path, logo_path=None):
        self.output_path = output_path
        self.logo_path = logo_path
        self.styles = self._crear_estilos()

    # =========================================================
    # ESTILOS
    # =========================================================
    def _crear_estilos(self):
        """Define los estilos de párrafo del reporte."""
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="TituloInstitucional",
            fontName="Helvetica-Bold", fontSize=13, leading=16,
            alignment=TA_CENTER, textColor=COLOR_AZUL_MARINO, spaceAfter=3,
        ))
        styles.add(ParagraphStyle(
            name="SubtituloReporte",
            fontName="Helvetica-Bold", fontSize=10, leading=13,
            alignment=TA_CENTER, textColor=COLOR_AZUL_MEDIO, spaceAfter=2,
        ))
        styles.add(ParagraphStyle(
            name="SubtituloUnidad",
            fontName="Helvetica", fontSize=9, leading=11,
            alignment=TA_CENTER, textColor=COLOR_GRIS_TEXTO, spaceAfter=8,
        ))
        styles.add(ParagraphStyle(
            name="TituloSeccion",
            fontName="Helvetica-Bold", fontSize=10, leading=13,
            textColor=COLOR_AZUL_MARINO, spaceBefore=14, spaceAfter=8,
        ))
        styles.add(ParagraphStyle(
            name="TextoNormal",
            fontName="Helvetica", fontSize=9.5, leading=14,
            textColor=COLOR_TEXTO, alignment=TA_JUSTIFY, spaceAfter=6,
        ))
        styles.add(ParagraphStyle(
            name="MetaTexto",
            fontName="Helvetica", fontSize=8, leading=11,
            textColor=COLOR_GRIS_TEXTO,
        ))
        styles.add(ParagraphStyle(
            name="MetaTextoRight",
            fontName="Helvetica", fontSize=8, leading=11,
            textColor=COLOR_GRIS_TEXTO, alignment=TA_RIGHT,
        ))
        styles.add(ParagraphStyle(
            name="KPIValor",
            fontName="Helvetica-Bold", fontSize=16, leading=18,
            alignment=TA_CENTER, textColor=COLOR_AZUL_MARINO,
        ))
        styles.add(ParagraphStyle(
            name="KPILabel",
            fontName="Helvetica", fontSize=7.5, leading=9,
            alignment=TA_CENTER, textColor=COLOR_GRIS_TEXTO,
        ))
        styles.add(ParagraphStyle(
            name="TablaEncabezado",
            fontName="Helvetica-Bold", fontSize=8.5, leading=11,
            textColor=white,
        ))
        styles.add(ParagraphStyle(
            name="TablaCelda",
            fontName="Helvetica", fontSize=9, leading=12,
            textColor=COLOR_TEXTO,
        ))
        styles.add(ParagraphStyle(
            name="TablaCeldaRight",
            fontName="Helvetica", fontSize=9, leading=12,
            textColor=COLOR_TEXTO, alignment=TA_RIGHT,
        ))
        styles.add(ParagraphStyle(
            name="Recomendacion",
            fontName="Helvetica", fontSize=9.5, leading=14,
            textColor=COLOR_TEXTO, leftIndent=12, spaceAfter=4,
        ))
        styles.add(ParagraphStyle(
            name="Footer",
            fontName="Helvetica", fontSize=7.5, leading=10,
            alignment=TA_CENTER, textColor=COLOR_GRIS_TEXTO,
        ))

        return styles

    # =========================================================
    # HEADER DEL DOCUMENTO
    # =========================================================
    def _crear_header(self, titulo, subtitulo, dirigido_a, fecha):
        elementos = []

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image(self.logo_path, width=20*mm, height=20*mm)
                logo.hAlign = "CENTER"
                elementos.append(logo)
                elementos.append(Spacer(1, 4*mm))
            except Exception:
                pass
        else:
            elementos.append(self._crear_isotipo_circular())
            elementos.append(Spacer(1, 4*mm))

        elementos.append(Paragraph(
            "ESCUELA MILITAR DE INGENIERÍA",
            self.styles["TituloInstitucional"]
        ))
        elementos.append(Paragraph(
            "Reporte de Percepción Institucional",
            self.styles["SubtituloReporte"]
        ))
        elementos.append(Paragraph(
            "Unidad Académica La Paz",
            self.styles["SubtituloUnidad"]
        ))

        linea = Table([[""]], colWidths=[170*mm], rowHeights=[1.5])
        linea.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_AZUL_MARINO),
        ]))
        elementos.append(linea)
        elementos.append(Spacer(1, 4*mm))

        meta_izq = Paragraph(
            f"<b>Dirigido a:</b> {dirigido_a}", self.styles["MetaTexto"]
        )
        meta_der = Paragraph(
            f"<b>Generado:</b> {fecha}", self.styles["MetaTextoRight"]
        )

        tabla_meta = Table([[meta_izq, meta_der]], colWidths=[100*mm, 70*mm])
        tabla_meta.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, COLOR_GRIS_BORDE),
        ]))
        elementos.append(tabla_meta)
        elementos.append(Spacer(1, 6*mm))

        return elementos

    def _crear_isotipo_circular(self):
        isotipo = Table(
            [[Paragraph(
                '<font color="#FFFFFF" size="14"><b>EMI</b></font>',
                ParagraphStyle(
                    name="Isotipo", alignment=TA_CENTER,
                    fontName="Helvetica-Bold", fontSize=14, leading=18,
                )
            )]],
            colWidths=[20*mm], rowHeights=[20*mm],
        )
        isotipo.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_AZUL_MARINO),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        isotipo.hAlign = "CENTER"
        return isotipo

    # =========================================================
    # TÍTULO DE SECCIÓN
    # =========================================================
    def _titulo_seccion(self, texto):
        tabla = Table(
            [[Paragraph(texto, self.styles["TituloSeccion"])]],
            colWidths=[170*mm],
        )
        tabla.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, COLOR_AZUL_MARINO),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return tabla

    # =========================================================
    # SECCIÓN: RESUMEN EJECUTIVO
    # =========================================================
    def _crear_resumen_ejecutivo(self, texto, num=1):
        elementos = []
        elementos.append(self._titulo_seccion(f"{num}. RESUMEN EJECUTIVO"))
        elementos.append(Paragraph(texto, self.styles["TextoNormal"]))
        return elementos

    # =========================================================
    # SECCIÓN: INDICADORES PRINCIPALES (KPIs)
    # =========================================================
    def _crear_indicadores(self, total, positivas, negativas, neutrales, num=2):
        elementos = []
        elementos.append(self._titulo_seccion(f"{num}. INDICADORES PRINCIPALES"))

        def crear_tarjeta(valor, etiqueta):
            contenido = [
                Paragraph(str(valor), self.styles["KPIValor"]),
                Spacer(1, 2),
                Paragraph(etiqueta, self.styles["KPILabel"]),
            ]
            tabla = Table([[contenido]], colWidths=[40*mm], rowHeights=[22*mm])
            tabla.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_GRIS_FONDO),
                ("BOX", (0, 0), (-1, -1), 0.5, COLOR_GRIS_BORDE),
                ("LINEBEFORE", (0, 0), (0, -1), 3, COLOR_AZUL_MARINO),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]))
            return tabla

        tarjeta_total = crear_tarjeta(f"{total:,}", "PUBLICACIONES")
        tarjeta_pos = crear_tarjeta(f"{positivas:,}", "POSITIVAS")
        tarjeta_neg = crear_tarjeta(f"{negativas:,}", "NEGATIVAS")
        tarjeta_neu = crear_tarjeta(f"{neutrales:,}", "NEUTRALES")

        tabla_kpis = Table(
            [[tarjeta_total, tarjeta_pos, tarjeta_neg, tarjeta_neu]],
            colWidths=[42*mm, 42*mm, 42*mm, 42*mm],
        )
        tabla_kpis.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ]))

        elementos.append(tabla_kpis)
        return elementos

    # =========================================================
    # SECCIÓN: FACTORES DE PERCEPCIÓN (TABLA)
    # =========================================================
    def _crear_factores(self, factores, num=3):
        elementos = []
        elementos.append(self._titulo_seccion(
            f"{num}. FACTORES DE PERCEPCIÓN IDENTIFICADOS"
        ))

        encabezados = [
            Paragraph("<b>Factor</b>", self.styles["TablaEncabezado"]),
            Paragraph("<b>Menciones</b>", self.styles["TablaEncabezado"]),
            Paragraph("<b>% Total</b>", self.styles["TablaEncabezado"]),
            Paragraph("<b>Sentimiento Neto</b>", self.styles["TablaEncabezado"]),
        ]

        filas = [encabezados]
        for nombre, menciones, pct_total, sent_neto in factores:
            signo = "+" if sent_neto > 0 else ""
            color = "#28A745" if sent_neto >= 0 else "#DC3545"
            sent_html = f'<font color="{color}"><b>{signo}{sent_neto}%</b></font>'

            filas.append([
                Paragraph(nombre, self.styles["TablaCelda"]),
                Paragraph(str(menciones), self.styles["TablaCeldaRight"]),
                Paragraph(f"{pct_total}%", self.styles["TablaCeldaRight"]),
                Paragraph(sent_html, self.styles["TablaCeldaRight"]),
            ])

        tabla = Table(
            filas,
            colWidths=[70*mm, 30*mm, 30*mm, 40*mm],
            repeatRows=1,
        )
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_AZUL_MARINO),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TEXTCOLOR", (0, 1), (-1, -1), COLOR_TEXTO),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, 0), 1, COLOR_AZUL_OSCURO),
            ("LINEBELOW", (0, 1), (-1, -1), 0.3, COLOR_GRIS_BORDE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, COLOR_GRIS_FONDO]),
        ]))

        elementos.append(tabla)
        return elementos

    # =========================================================
    # SECCIÓN: MÉTRICAS DEL MODELO NLP (NUEVA)
    # =========================================================
    def _crear_metricas_modelo(self, num=4):
        """Crea la sección de métricas del modelo NLP."""
        elementos = []
        elementos.append(self._titulo_seccion(f"{num}. MÉTRICAS DEL MODELO NLP"))

        elementos.append(Paragraph(
            "Las siguientes métricas corresponden al modelo BETO (clasificación de "
            "polaridad) y BERTopic (modelado de temas) utilizados para el análisis "
            "del corpus.",
            self.styles["TextoNormal"]
        ))
        elementos.append(Spacer(1, 4*mm))

        encabezados = [
            Paragraph("<b>Métrica</b>", self.styles["TablaEncabezado"]),
            Paragraph("<b>Valor</b>", self.styles["TablaEncabezado"]),
            Paragraph("<b>Descripción</b>", self.styles["TablaEncabezado"]),
        ]

        filas = [encabezados]
        metricas = [
            ("F1-Score (BETO)", "0.9489", "Balance entre precisión y recall"),
            ("Precisión (BETO)", "0.95", "Proporción de positivos correctos"),
            ("Recall (BETO)", "0.94", "Proporción de positivos detectados"),
            ("CV Score (BERTopic)", "0.6667", "Coherencia del modelado de temas"),
        ]

        for nombre, valor, desc in metricas:
            filas.append([
                Paragraph(nombre, self.styles["TablaCelda"]),
                Paragraph(f"<b>{valor}</b>", self.styles["TablaCeldaRight"]),
                Paragraph(desc, self.styles["TablaCelda"]),
            ])

        tabla = Table(filas, colWidths=[60*mm, 30*mm, 80*mm], repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_AZUL_MARINO),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TEXTCOLOR", (0, 1), (-1, -1), COLOR_TEXTO),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, 0), 1, COLOR_AZUL_OSCURO),
            ("LINEBELOW", (0, 1), (-1, -1), 0.3, COLOR_GRIS_BORDE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, COLOR_GRIS_FONDO]),
        ]))

        elementos.append(tabla)
        return elementos

    # =========================================================
    # SECCIÓN: RECOMENDACIONES
    # =========================================================
    def _crear_recomendaciones(self, recomendaciones, num=5):
        elementos = []
        elementos.append(self._titulo_seccion(f"{num}. RECOMENDACIONES"))

        for i, rec in enumerate(recomendaciones, 1):
            elementos.append(Paragraph(
                f"<b>{i}.</b> {rec}",
                self.styles["Recomendacion"]
            ))

        return elementos

    # =========================================================
    # SECCIÓN: ANEXOS (NUEVA)
    # =========================================================
    def _crear_anexos(self, num=6):
        """Crea la sección de anexos con datos detallados."""
        elementos = []
        elementos.append(self._titulo_seccion(f"{num}. ANEXOS"))

        elementos.append(Paragraph(
            "El presente reporte se complementa con los siguientes archivos "
            "digitales que contienen los datos crudos utilizados para el análisis:",
            self.styles["TextoNormal"]
        ))
        elementos.append(Spacer(1, 3*mm))

        anexos = [
            "<b>Anexo A:</b> Dataset completo de opiniones en formato CSV.",
            "<b>Anexo B:</b> Resultados detallados de la clasificación de polaridad.",
            "<b>Anexo C:</b> Factores temáticos identificados por BERTopic.",
        ]

        for anexo in anexos:
            elementos.append(Paragraph(
                f"• {anexo}",
                self.styles["Recomendacion"]
            ))

        return elementos

    # =========================================================
    # FOOTER EN CADA PÁGINA
    # =========================================================
    def _footer(self, canvas, doc):
        canvas.saveState()
        ancho, alto = A4

        canvas.setStrokeColor(COLOR_GRIS_BORDE)
        canvas.setLineWidth(0.5)
        canvas.line(2*cm, 1.8*cm, ancho - 2*cm, 1.8*cm)

        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(COLOR_GRIS_TEXTO)
        canvas.drawCentredString(
            ancho / 2, 1.3*cm,
            "Reporte generado automáticamente por el Sistema de Percepción Institucional - EMI-UALP"
        )
        canvas.drawCentredString(
            ancho / 2, 0.9*cm,
            "Documento confidencial para uso institucional"
        )

        canvas.setFont("Helvetica", 7)
        canvas.drawRightString(
            ancho - 2*cm, 0.9*cm,
            f"Página {doc.page}"
        )

        canvas.restoreState()

    # =========================================================
    # MÉTODO PRINCIPAL
    # =========================================================
    def generar(self, datos):
        """
        Genera el PDF completo.

        datos = {
            "titulo": str,
            "subtitulo": str,
            "dirigido_a": str,
            "total": int,
            "positivas": int,
            "negativas": int,
            "neutrales": int,
            "factores": [(nombre, menciones, pct_total, sent_neto), ...],
            "recomendaciones": [str, ...],
            "resumen": str,
            "secciones": {
                "resumen": bool,
                "distribucion": bool,
                "factores": bool,
                "metricas": bool,
                "recomendaciones": bool,
                "anexos": bool,
            }
        }
        """
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            leftMargin=20*mm,
            rightMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=25*mm,
            title=datos.get("titulo", "Reporte de Percepción Institucional"),
            author="EMI-UALP",
            subject="Percepción Institucional",
        )

        elementos = []

        # Secciones a incluir
        secciones = datos.get("secciones", {
            "resumen": True,
            "distribucion": True,
            "factores": True,
            "metricas": True,
            "recomendaciones": True,
            "anexos": False,
        })

        # Header (siempre)
        fecha = datetime.now().strftime("%d/%m/%Y")
        elementos.extend(self._crear_header(
            titulo=datos.get("titulo", "Reporte de Percepción Institucional"),
            subtitulo=datos.get("subtitulo", ""),
            dirigido_a=datos.get("dirigido_a", "Dirección Académica EMI-UALP"),
            fecha=fecha,
        ))

        # Numeración dinámica
        num_seccion = 1

        # Resumen ejecutivo
        if secciones.get("resumen", True):
            elementos.extend(self._crear_resumen_ejecutivo(
                datos.get("resumen", ""), num_seccion
            ))
            elementos.append(Spacer(1, 4*mm))
            num_seccion += 1

        # Indicadores
        if secciones.get("distribucion", True) or secciones.get("metricas", True):
            elementos.extend(self._crear_indicadores(
                datos.get("total", 0),
                datos.get("positivas", 0),
                datos.get("negativas", 0),
                datos.get("neutrales", 0),
                num_seccion
            ))
            elementos.append(Spacer(1, 6*mm))
            num_seccion += 1

        # Factores
        if secciones.get("factores", True):
            elementos.extend(self._crear_factores(
                datos.get("factores", []), num_seccion
            ))
            elementos.append(Spacer(1, 6*mm))
            num_seccion += 1

        # Métricas del modelo
        if secciones.get("metricas", True):
            elementos.extend(self._crear_metricas_modelo(num_seccion))
            elementos.append(Spacer(1, 6*mm))
            num_seccion += 1

        # Recomendaciones
        if secciones.get("recomendaciones", True):
            elementos.extend(self._crear_recomendaciones(
                datos.get("recomendaciones", []), num_seccion
            ))
            num_seccion += 1

        # Anexos
        if secciones.get("anexos", False):
            elementos.extend(self._crear_anexos(num_seccion))

        # Generar PDF
        doc.build(
            elementos,
            onFirstPage=self._footer,
            onLaterPages=self._footer
        )

        return self.output_path