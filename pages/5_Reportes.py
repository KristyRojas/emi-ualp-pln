# pages/5_Reportes.py
import streamlit as st
import pandas as pd
import sys
import os
import json
import base64
from datetime import datetime
from src.ui.sidebar import render_sidebar
from src.ui.styles import inyectar_css_global

# === NUEVO IMPORT PARA EL GENERADOR PDF PROFESIONAL ===
from src.reports.pdf_generator import ReportePDF

# === MARCAR PÁGINA ACTIVA ===
st.session_state.page = "reportes"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datasets.dataset_manager import DatasetManager


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Reportes - EMI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# VALIDAR SESIÓN
# =========================================================
if not st.session_state.get("authenticated", False):
    st.warning("Debe iniciar sesión para acceder")
    st.stop()

user_actual = st.session_state.user


# =========================================================
# UTILIDADES
# =========================================================
def get_logo_base64():
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets", "logo_emi.png"
    )
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def cargar_datos_pln():
    """Carga el corpus procesado por PLN más reciente."""
    dm = DatasetManager()
    archivos = []

    if os.path.exists(dm.processed_dir):
        for f in os.listdir(dm.processed_dir):
            if f.endswith(".csv"):
                ruta = os.path.join(dm.processed_dir, f)
                try:
                    df_check = pd.read_csv(ruta, encoding="utf-8-sig", nrows=1)
                    if "sentimiento" in df_check.columns and "factor" in df_check.columns:
                        archivos.append((ruta, os.path.getmtime(ruta)))
                except Exception:
                    continue

    if not archivos:
        return None, None

    archivos.sort(key=lambda x: x[1], reverse=True)
    ruta_reciente = archivos[0][0]
    df = pd.read_csv(ruta_reciente, encoding="utf-8-sig")

    if "texto" not in df.columns and "texto_original" in df.columns:
        df["texto"] = df["texto_original"]

    return df, os.path.basename(ruta_reciente)


def cargar_historial_reportes():
    """Carga el historial de reportes generados."""
    archivo = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "reportes_historial.json"
    )
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_historial_reportes(historial):
    archivo = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "reportes_historial.json"
    )
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)


def sentimiento_neto_por_factor(df, factor):
    df_f = df[df["factor"] == factor]
    if len(df_f) == 0:
        return 0
    pos = len(df_f[df_f["sentimiento"] == "positivo"])
    neg = len(df_f[df_f["sentimiento"] == "negativo"])
    return round(((pos - neg) / len(df_f)) * 100, 1)


# =========================================================
# HEADER
# =========================================================
def render_header(user, logo_b64):
    col_logo, col_user = st.columns([4, 1])

    with col_logo:
        if logo_b64:
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="max-height: 42px;" />'
        else:
            logo_html = '<div style="font-size: 26px; font-weight: 900; color: #FFFFFF; letter-spacing: 2px; font-family: Arial, sans-serif;">EMI</div>'

        st.markdown(
            '<div class="emi-top-header" style="background: #035AA6; padding: 14px 24px; '
            'margin: 0 -1.5rem 0 -1.5rem; border-bottom: 3px solid #F2B705; '
            'display: flex; align-items: center; gap: 14px; '
            'box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
            f'{logo_html}'
            '<div>'
            '<div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">'
            'Percepción Institucional</div>'
            '<div style="font-size: 10.5px; color: rgba(255,255,255,0.85);">'
            'Sistema EMI - La Paz</div>'
            '</div></div>',
            unsafe_allow_html=True
        )

    with col_user:
        inicial = user['nombre'][0].upper() if user.get('nombre') else "A"
        st.markdown(
            '<div class="emi-top-header" style="background: #035AA6; padding: 14px 24px; '
            'margin: 0 -1.5rem 0 -1.5rem; border-bottom: 3px solid #F2B705; '
            'display: flex; justify-content: flex-end; align-items: center; '
            'gap: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
            f'<span style="color: #FFFFFF; font-size: 13px; font-weight: 600;">'
            f'{user.get("rol", "Administrador")}</span>'
            '<div style="width: 36px; height: 36px; border-radius: 50%; '
            'background: #F2B705; color: #035AA6; display: flex; '
            'align-items: center; justify-content: center; '
            f'font-weight: 900; font-size: 14px;">{inicial}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# HERO
# =========================================================
def render_hero(eyebrow, titulo, descripcion=""):
    desc_html = f'<p style="font-size: 13px; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; margin: 0; line-height: 1.5;">{descripcion}</p>' if descripcion else ''
    st.markdown(
        '<div class="emi-hero" style="background: linear-gradient(135deg, #003366 0%, #035AA6 100%); '
        'padding: 24px 28px; border-radius: 10px; margin: 24px 0 8px 0; '
        'box-shadow: 0 4px 12px rgba(0,51,102,0.25); '
        'color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;">'
        f'<div style="font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; '
        f'color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; '
        f'margin-bottom: 8px; font-weight: 600;">{eyebrow}</div>'
        f'<h1 style="font-size: 24px; font-weight: 700; '
        f'color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; '
        f'margin: 0 0 8px 0 !important; padding: 0 !important; '
        f'border: none !important; line-height: 1.2;">{titulo}</h1>'
        f'{desc_html}'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# RENDERIZAR
# =========================================================
logo_b64 = get_logo_base64()

inyectar_css_global()
render_sidebar(user_actual, logo_b64, current_page="reportes")
render_header(user_actual, logo_b64)


# =========================================================
# CARGAR DATOS
# =========================================================
df_corpus, nombre_archivo = cargar_datos_pln()

if df_corpus is None or len(df_corpus) == 0:
    render_hero(
        "INFORMES Y REPORTES",
        "Informes y Reportes Institucionales",
        "Generación de reportes ejecutivos sobre la percepción institucional."
    )
    st.warning(
        "No hay corpus procesado disponible. "
        "Ejecute primero el **Procesamiento y Análisis PLN** y guarde el análisis."
    )
    st.stop()


# =========================================================
# CÁLCULO DE MÉTRICAS
# =========================================================
total = len(df_corpus)
conteo = df_corpus["sentimiento"].value_counts().to_dict()
pos = conteo.get("positivo", 0)
neg = conteo.get("negativo", 0)
neu = conteo.get("neutral", 0)

pct_pos = round((pos / total) * 100, 1) if total > 0 else 0
pct_neg = round((neg / total) * 100, 1) if total > 0 else 0
pct_neu = round((neu / total) * 100, 1) if total > 0 else 0

factores = df_corpus["factor"].value_counts().to_dict()
factores = {k: v for k, v in factores.items() if k != "Sin clasificar"}

factores_con_sent = []
for f, v in factores.items():
    sent_neto = sentimiento_neto_por_factor(df_corpus, f)
    factores_con_sent.append((f, v, sent_neto))

factores_con_sent.sort(key=lambda x: x[2])


# =========================================================
# HERO
# =========================================================
render_hero(
    "INFORMES Y REPORTES INSTITUCIONALES",
    "Análisis y generación de reportes institucionales",
    "Genere reportes ejecutivos sobre la percepción institucional para apoyar la toma de decisiones."
)

st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)


# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "ANALISIS INSTITUCIONAL",
    "CONFIGURAR REPORTE",
    "HISTORIAL DE REPORTES"
])


# =========================================================
# TAB 1: ANÁLISIS DE RESULTADOS INSTITUCIONALES
# =========================================================
with tab1:
    st.markdown("### Análisis de Resultados Institucionales")
    st.markdown("Resumen consolidado de la percepción institucional.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Publicaciones Analizadas</div>'
            f'<div class="value">{total:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">Percepción Positiva</div>'
            f'<div class="value">{pct_pos}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card rojo">'
            '<div class="label">Percepción Negativa</div>'
            f'<div class="value">{pct_neg}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Factores Identificados</div>'
            f'<div class="value">{len(factores)}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    st.markdown("#### Resumen Ejecutivo")

    if pct_pos > pct_neg and pct_pos > pct_neu:
        tendencia = "positiva"
    elif pct_neg > pct_pos and pct_neg > pct_neu:
        tendencia = "negativa"
    else:
        tendencia = "neutral"

    top_factores_texto = ""
    if factores_con_sent:
        top = factores_con_sent[:3]
        top_factores_texto = ", ".join([f"{f} ({v} menciones, {s:+.1f}% sent.)" for f, v, s in top])

    resumen_texto = (
        f"Se analizaron <strong>{total:,} publicaciones</strong> recopiladas de Facebook y Google Maps. "
        f"La percepción general de la EMI-UALP es mayormente <strong>{tendencia}</strong>, "
        f"con un {max(pct_pos, pct_neu, pct_neg)}% de opiniones "
        f"{'positivas' if tendencia == 'positiva' else 'neutrales' if tendencia == 'neutral' else 'negativas'}. "
    )

    if top_factores_texto:
        resumen_texto += f"Los factores más relevantes son: <strong>{top_factores_texto}</strong>. "

    resumen_texto += (
        "Se recomienda priorizar la revisión de los factores con sentimiento neto negativo "
        "y mantener el monitoreo continuo de la percepción digital."
    )

    st.markdown(
        f'<div class="info-card">{resumen_texto}</div>',
        unsafe_allow_html=True
    )

    st.markdown("#### Factores Relevantes")
    st.markdown("Factores identificados ordenados por sentimiento neto (más negativo primero).")

    if factores_con_sent:
        filas = ""
        for factor, menciones, sent_neto in factores_con_sent[:10]:
            pct_total = round((menciones / total) * 100, 1)

            # Determinar clase según el valor
            if sent_neto > 0:
                clase_sent = "sent-neto-positivo"
                signo = "+"
            elif sent_neto < 0:
                clase_sent = "sent-neto-negativo"
                signo = ""
            else:
                clase_sent = "sent-neto-cero"
                signo = ""

            filas += (
                '<tr>'
                f'<td style="font-weight: 600; color: #0B2440 !important; '
                f'-webkit-text-fill-color: #0B2440 !important;">{factor}</td>'
                f'<td style="text-align: right; color:#0B2440 !important; '
                f'-webkit-text-fill-color: #0B2440 !important;">{menciones}</td>'
                f'<td style="text-align: right; color:#666 !important; '
                f'-webkit-text-fill-color: #666 !important;">{pct_total}%</td>'
                f'<td class="{clase_sent}">{signo}{sent_neto}%</td>'
                '</tr>'
            )

        tabla = (
            '<div class="result-table">'
            '<table>'
            '<thead><tr>'
            '<th style="text-align: left;">Factor</th>'
            '<th style="text-align: right;">Menciones</th>'
            '<th style="text-align: right;">% Total</th>'
            '<th style="text-align: right;">Sent. Neto</th>'
            '</tr></thead>'
            '<tbody>' + filas + '</tbody>'
            '</table></div>'
        )
        st.markdown(tabla, unsafe_allow_html=True)


# =========================================================
# TAB 2: CONFIGURAR REPORTE
# =========================================================
with tab2:
    st.markdown("### Configurar Reporte")
    st.markdown("Complete los datos del reporte institucional.")
    st.markdown("---")

    with st.form("form_config_reporte", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            titulo_reporte = st.text_input(
                "Título del Reporte *",
                value="Reporte de Percepción Institucional — EMI UALP"
            )
            periodo = st.selectbox(
                "Periodo de Análisis *",
                ["Último trimestre", "Último semestre", "Último año",
                 "Gestión 2024", "Gestión 2025", "Gestión 2026",
                 "Personalizado"]
            )
            fuente = st.selectbox(
                "Fuentes de Datos *",
                ["Todas las fuentes", "Solo Facebook", "Solo Google Maps"]
            )

        with col2:
            dirigido_a = st.text_input(
                "Dirigido a *",
                value="Dirección Académica EMI-UALP"
            )
            formato = st.selectbox(
                "Formato de salida *",
                ["PDF", "CSV", "PDF + CSV"]
            )
            incluir_graficos = st.checkbox("Incluir gráficos en el reporte", value=True)

        observaciones = st.text_area(
            "Observaciones (opcional)",
            placeholder="Ingrese observaciones o comentarios adicionales...",
            height=100
        )

        st.markdown("---")
        st.markdown("#### Secciones a incluir")
        col_s1, col_s2, col_s3 = st.columns(3)

        with col_s1:
            incluir_resumen = st.checkbox("Resumen ejecutivo", value=True)
            incluir_dist = st.checkbox("Distribución de sentimientos", value=True)

        with col_s2:
            incluir_factores = st.checkbox("Factores de percepción", value=True)
            incluir_metricas = st.checkbox("Métricas del modelo", value=True)

        with col_s3:
            incluir_recomendaciones = st.checkbox("Recomendaciones", value=True)
            incluir_anexos = st.checkbox("Anexos con datos detallados", value=False)

        st.markdown("---")
        submitted = st.form_submit_button(
            "GENERAR REPORTE",
            type="primary",
            use_container_width=True
        )

    # ==== GENERAR REPORTE ====
    if submitted:
        errores = []
        if not titulo_reporte:
            errores.append("El título del reporte es obligatorio")
        if not dirigido_a:
            errores.append("El destinatario es obligatorio")

        if errores:
            for e in errores:
                st.error(e)
        else:
            with st.spinner("Generando reporte..."):
                progress = st.progress(0)
                status = st.empty()

                # PASO 1
                status.markdown("**Paso 1/4:** Consolidando datos...")
                progress.progress(25)

                df_rep = df_corpus.copy()
                if fuente == "Solo Facebook":
                    df_rep = df_rep[df_rep["fuente"] == "facebook"]
                elif fuente == "Solo Google Maps":
                    df_rep = df_rep[df_rep["fuente"] == "google_maps"]

                total_rep = len(df_rep)
                conteo_rep = df_rep["sentimiento"].value_counts().to_dict()
                pos_rep = conteo_rep.get("positivo", 0)
                neg_rep = conteo_rep.get("negativo", 0)
                neu_rep = conteo_rep.get("neutral", 0)
                pct_pos_rep = round((pos_rep / total_rep) * 100, 1) if total_rep > 0 else 0
                pct_neg_rep = round((neg_rep / total_rep) * 100, 1) if total_rep > 0 else 0
                pct_neu_rep = round((neu_rep / total_rep) * 100, 1) if total_rep > 0 else 0

                # PASO 2
                status.markdown("**Paso 2/4:** Generando contenido...")
                progress.progress(50)

                factores_rep = df_rep["factor"].value_counts().to_dict()
                factores_rep = {k: v for k, v in factores_rep.items() if k != "Sin clasificar"}

                factores_reporte = []
                for f, v in factores_rep.items():
                    sent_neto = sentimiento_neto_por_factor(df_rep, f)
                    pct_total = round((v / total_rep) * 100, 1)
                    factores_reporte.append((f, v, pct_total, sent_neto))

                factores_reporte.sort(key=lambda x: -x[1])

                if pct_pos_rep > pct_neg_rep and pct_pos_rep > pct_neu_rep:
                    tendencia = "positiva"
                elif pct_neg_rep > pct_pos_rep and pct_neg_rep > pct_neu_rep:
                    tendencia = "negativa"
                else:
                    tendencia = "neutral"

                resumen_txt = (
                    f"El presente reporte sintetiza los resultados del análisis de percepción "
                    f"institucional realizado sobre {total_rep:,} publicaciones recopiladas "
                    f"de Facebook y Google Maps. La percepción general de la EMI-UALP es mayormente "
                    f"{tendencia}, con un {max(pct_pos_rep, pct_neu_rep, pct_neg_rep)}% de "
                    f"opiniones {'positivas' if tendencia == 'positiva' else 'neutrales' if tendencia == 'neutral' else 'negativas'}."
                )

                recomendaciones = []
                factores_por_sent = sorted(factores_reporte, key=lambda x: x[3])
                if factores_por_sent and factores_por_sent[0][3] < 0:
                    f_top = factores_por_sent[0]
                    recomendaciones.append(
                        f"Priorizar la revisión del factor <b>{f_top[0]}</b>, cuyo sentimiento "
                        f"neto es de {f_top[3]:+.1f}%."
                    )
                factores_pos = sorted(factores_reporte, key=lambda x: -x[3])
                if factores_pos and factores_pos[0][3] > 0:
                    f_pos = factores_pos[0]
                    recomendaciones.append(
                        f"Identificar y replicar las acciones mejor valoradas asociadas al factor "
                        f"<b>{f_pos[0]}</b>, con un sentimiento neto de {f_pos[3]:+.1f}%."
                    )
                recomendaciones.append(
                    "Establecer un monitoreo periódico de los factores con sentimiento neto "
                    "negativo para detectar cambios en la percepción institucional."
                )
                if observaciones:
                    recomendaciones.append(f"Considerar las observaciones del usuario: {observaciones}")

                # PASO 3
                status.markdown("**Paso 3/4:** Generando PDF profesional...")
                progress.progress(75)

                dm = DatasetManager()
                nombre_reporte = f"reporte_{datetime.now():%Y%m%d_%H%M%S}"
                pdf_path = os.path.join(dm.processed_dir, f"{nombre_reporte}.pdf")

                logo_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets", "logo_emi.png"
                )

                generador = ReportePDF(pdf_path, logo_path=logo_path if os.path.exists(logo_path) else None)

                datos_pdf = {
                    "titulo": titulo_reporte,
                    "subtitulo": "Unidad Académica La Paz",
                    "dirigido_a": dirigido_a,
                    "total": total_rep,
                    "positivas": pos_rep,
                    "negativas": neg_rep,
                    "neutrales": neu_rep,
                    "pct_pos": pct_pos_rep,
                    "pct_neg": pct_neg_rep,
                    "pct_neu": pct_neu_rep,
                    "factores": factores_reporte[:8],
                    "recomendaciones": recomendaciones,
                    "resumen": resumen_txt,
                    "tendencia": tendencia,
                    "periodo": periodo,
                }

                generador.generar(datos_pdf)

                csv_path = os.path.join(dm.processed_dir, f"{nombre_reporte}.csv")
                df_rep.to_csv(csv_path, index=False, encoding="utf-8-sig")

                # PASO 4
                status.markdown("**Paso 4/4:** Registrando en historial...")
                progress.progress(95)

                historial = cargar_historial_reportes()
                historial.insert(0, {
                    "nombre": nombre_reporte,
                    "titulo": titulo_reporte,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "periodo": periodo,
                    "fuente": fuente,
                    "dirigido_a": dirigido_a,
                    "formato": formato,
                    "registros": total_rep,
                    "archivo_pdf": pdf_path,
                    "archivo_csv": csv_path,
                })
                guardar_historial_reportes(historial)

                progress.progress(100)
                status.markdown("**Completado**")

            st.success(f"Reporte generado exitosamente: **{nombre_reporte}**")
            st.balloons()

            # ==== BOTONES DE DESCARGA CON KEY ÚNICO ====
            st.markdown("---")
            st.markdown("### Descargar Reporte Generado")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f_pdf:
                        st.download_button(
                            label="Descargar PDF",
                            data=f_pdf.read(),
                            file_name=f"{nombre_reporte}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary",
                            key=f"dl_pdf_generado_{nombre_reporte}"
                        )

            with col_dl2:
                if os.path.exists(csv_path):
                    with open(csv_path, "rb") as f_csv:
                        st.download_button(
                            label="Descargar CSV (datos)",
                            data=f_csv.read(),
                            file_name=f"{nombre_reporte}.csv",
                            mime="text/csv",
                            use_container_width=True,
                            key=f"dl_csv_generado_{nombre_reporte}"
                        )


# =========================================================
# TAB 3: HISTORIAL DE REPORTES
# =========================================================
with tab3:
    st.markdown("### Historial de Reportes Generados")
    st.markdown("Consulte y descargue los reportes generados anteriormente.")
    st.markdown("---")

    historial = cargar_historial_reportes()

    if not historial:
        st.info("Aún no se han generado reportes. Vaya a la pestaña **CONFIGURAR REPORTE** para crear uno.")
    else:
        # ==== MÉTRICAS ====
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">Reportes Generados</div>'
                f'<div class="value">{len(historial)}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col2:
            total_regs = sum(r.get("registros", 0) for r in historial)
            st.markdown(
                '<div class="metric-card verde">'
                '<div class="label">Registros Totales</div>'
                f'<div class="value">{total_regs:,}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col3:
            formatos = set(r.get("formato", "") for r in historial)
            st.markdown(
                '<div class="metric-card amarillo">'
                '<div class="label">Formatos Distintos</div>'
                f'<div class="value">{len(formatos)}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # ==== LISTA DE REPORTES ====
        for i, r in enumerate(historial):
            titulo_exp = r.get('titulo', r.get('nombre', 'Sin título'))
            fecha_exp = r.get('fecha', '')
            regs_exp = r.get('registros', 0)

            with st.expander(
                f"**{titulo_exp}** · {fecha_exp} · {regs_exp:,} registros",
                expanded=False
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
**Detalles del reporte:**
- **Nombre interno:** `{r.get('nombre', '')}`
- **Título:** {r.get('titulo', '')}
- **Fecha:** {r.get('fecha', '')}
- **Periodo:** {r.get('periodo', '')}
- **Fuente:** {r.get('fuente', '')}
                    """)

                with col2:
                    st.markdown(f"""
**Información:**
- **Dirigido a:** {r.get('dirigido_a', '')}
- **Formato:** {r.get('formato', '')}
- **Registros:** {r.get('registros', 0):,}
                    """)

                # ==== BOTONES DE DESCARGA CON KEY ÚNICO POR REPORTE ====
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    pdf_path_h = r.get("archivo_pdf", "")
                    if pdf_path_h and os.path.exists(pdf_path_h):
                        with open(pdf_path_h, "rb") as f_pdf_h:
                            st.download_button(
                                label="Descargar PDF",
                                data=f_pdf_h.read(),
                                file_name=os.path.basename(pdf_path_h),
                                mime="application/pdf",
                                use_container_width=True,
                                key=f"hist_dl_pdf_{i}_{r.get('nombre', i)}"
                            )
                    else:
                        st.button("PDF no disponible", disabled=True,
                                  use_container_width=True,
                                  key=f"hist_no_pdf_{i}_{r.get('nombre', i)}")

                with col_b:
                    csv_path_h = r.get("archivo_csv", "")
                    if csv_path_h and os.path.exists(csv_path_h):
                        with open(csv_path_h, "rb") as f_csv_h:
                            st.download_button(
                                label="Descargar CSV",
                                data=f_csv_h.read(),
                                file_name=os.path.basename(csv_path_h),
                                mime="text/csv",
                                use_container_width=True,
                                key=f"hist_dl_csv_{i}_{r.get('nombre', i)}"
                            )
                    else:
                        st.button("CSV no disponible", disabled=True,
                                  use_container_width=True,
                                  key=f"hist_no_csv_{i}_{r.get('nombre', i)}")

                with col_c:
                    if st.button("Eliminar",
                                  use_container_width=True,
                                  key=f"hist_del_{i}_{r.get('nombre', i)}"):
                        st.session_state[f"confirm_del_rep_{i}"] = True

                # ==== CONFIRMACIÓN DE ELIMINACIÓN ====
                if st.session_state.get(f"confirm_del_rep_{i}"):
                    st.warning(f"¿Eliminar el reporte **{titulo_exp}**?")
                    cx, cy = st.columns(2)
                    with cx:
                        if st.button("Sí, eliminar", type="primary",
                                      use_container_width=True,
                                      key=f"hist_conf_si_{i}_{r.get('nombre', i)}"):
                            hist_actual = cargar_historial_reportes()
                            if i < len(hist_actual):
                                hist_actual.pop(i)
                                guardar_historial_reportes(hist_actual)
                            st.session_state[f"confirm_del_rep_{i}"] = False
                            st.success("Reporte eliminado")
                            st.rerun()
                    with cy:
                        if st.button("Cancelar", use_container_width=True,
                                      key=f"hist_conf_no_{i}_{r.get('nombre', i)}"):
                            st.session_state[f"confirm_del_rep_{i}"] = False
                            st.rerun()

        # ==== LIMPIAR HISTORIAL COMPLETO ====
        st.markdown("---")
        if st.button("Limpiar todo el historial", type="primary", key="btn_clear_hist"):
            st.session_state["confirm_clear_rep_hist"] = True

        if st.session_state.get("confirm_clear_rep_hist"):
            st.warning("¿Está seguro de borrar TODO el historial? Esta acción no se puede deshacer.")
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button("Sí, borrar todo", type="primary",
                              use_container_width=True, key="clear_hist_si"):
                    guardar_historial_reportes([])
                    st.session_state["confirm_clear_rep_hist"] = False
                    st.success("Historial borrado")
                    st.rerun()
            with col_y:
                if st.button("Cancelar", use_container_width=True, key="clear_hist_no"):
                    st.session_state["confirm_clear_rep_hist"] = False
                    st.rerun()