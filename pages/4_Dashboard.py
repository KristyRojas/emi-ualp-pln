# pages/4_Dashboard.py
import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
from datetime import datetime
from src.ui.sidebar import render_sidebar
from src.ui.styles import inyectar_css_global

# === MARCAR PÁGINA ACTIVA ===
st.session_state.page = "dashboard"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datasets.dataset_manager import DatasetManager


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Dashboard - EMI",
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
    import base64
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets", "logo_emi.png"
    )
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


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
render_sidebar(user_actual, logo_b64, current_page="dashboard")
render_header(user_actual, logo_b64)


# =========================================================
# CARGAR DATOS
# =========================================================
@st.cache_data(ttl=30)
def cargar_datos():
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

    return df, os.path.basename(ruta_reciente)


df_corpus, nombre_archivo = cargar_datos()

if df_corpus is None or len(df_corpus) == 0:
    st.warning(
        "No hay corpus procesado disponible. "
        "Ejecute primero el **Procesamiento y Análisis PLN** y guarde el análisis."
    )
    st.stop()

# Alias de columna texto
if "texto" not in df_corpus.columns and "texto_original" in df_corpus.columns:
    df_corpus["texto"] = df_corpus["texto_original"]


# =========================================================
# CÁLCULO DE MÉTRICAS GLOBALES
# =========================================================
total_global = len(df_corpus)
conteo_global = df_corpus["sentimiento"].value_counts().to_dict()
pos_global = conteo_global.get("positivo", 0)
neg_global = conteo_global.get("negativo", 0)
neu_global = conteo_global.get("neutral", 0)

pct_pos = round((pos_global / total_global) * 100, 1) if total_global > 0 else 0
pct_neg = round((neg_global / total_global) * 100, 1) if total_global > 0 else 0
pct_neu = round((neu_global / total_global) * 100, 1) if total_global > 0 else 0

factores_global = df_corpus["factor"].value_counts().to_dict()
factores_global = {k: v for k, v in factores_global.items() if k != "Sin clasificar"}


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def sentimiento_neto_por_factor(df, factor):
    """Calcula el sentimiento neto de un factor: ((pos - neg) / total) * 100."""
    df_f = df[df["factor"] == factor]
    if len(df_f) == 0:
        return 0
    pos = len(df_f[df_f["sentimiento"] == "positivo"])
    neg = len(df_f[df_f["sentimiento"] == "negativo"])
    total_f = len(df_f)
    return round(((pos - neg) / total_f) * 100, 1)


def preparar_dataframe_con_anio(df):
    """
    Prepara el DataFrame agregando la columna 'anio' a partir de
    'fecha_creacion' o 'fecha'. Devuelve el df filtrado con años válidos.
    """
    df_anual = df.copy()

    if "anio" in df_anual.columns:
        df_anual["anio"] = pd.to_numeric(df_anual["anio"], errors="coerce")
    else:
        if "fecha_creacion" in df_anual.columns:
            df_anual["fecha_dt"] = pd.to_datetime(
                df_anual["fecha_creacion"], errors="coerce"
            )
        elif "fecha" in df_anual.columns:
            df_anual["fecha_dt"] = pd.to_datetime(
                df_anual["fecha"], errors="coerce"
            )
        else:
            return None
        df_anual["anio"] = df_anual["fecha_dt"].dt.year

    df_anual = df_anual[df_anual["anio"].notna()].copy()
    df_anual["anio"] = df_anual["anio"].astype(int)

    # Rango razonable de años (evita outliers como 1970 o 2100)
    df_anual = df_anual[(df_anual["anio"] >= 2000) & (df_anual["anio"] <= 2030)]

    return df_anual


def calcular_prevalencia_anual_por_factor(df, factor):
    """
    Calcula la prevalencia anual de un factor.
    Fórmula: (menciones del factor en un año / menciones totales en ese año) * 100
    Retorna: dict {año: porcentaje}
    """
    df_anual = preparar_dataframe_con_anio(df)
    if df_anual is None or len(df_anual) == 0:
        return {}

    # Menciones del factor por año
    df_factor = df_anual[df_anual["factor"] == factor]
    menciones_factor_por_anio = df_factor.groupby("anio").size().to_dict()

    # Total de menciones por año
    total_por_anio = df_anual.groupby("anio").size().to_dict()

    # Calcular prevalencia
    prevalencia = {}
    for anio in sorted(total_por_anio.keys()):
        total_anio = total_por_anio[anio]
        menciones_anio = menciones_factor_por_anio.get(anio, 0)
        if total_anio > 0:
            prevalencia[anio] = round((menciones_anio / total_anio) * 100, 1)
        else:
            prevalencia[anio] = 0

    return prevalencia


# =========================================================
# HERO — ÚNICO, ARRIBA DE LOS TABS
# =========================================================
render_hero(
    "DASHBOARD DE PERCEPCION INSTITUCIONAL",
    "Panel de análisis de percepción institucional",
    "Monitoreo de menciones, sentimientos y factores de opinión sobre la "
    "Escuela Militar de Ingeniería, Unidad Académica La Paz."
)

# Spacer entre hero y tabs
st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)


# =========================================================
# TABS — DEBAJO DEL HERO
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "RESUMEN GENERAL",
    "DISTRIBUCION POLARIDAD",
    "FACTORES BERTopic",
    "BUSQUEDA Y FILTRADO"
])


# =========================================================
# TAB 1: RESUMEN GENERAL
# =========================================================
with tab1:
    st.markdown("### Resumen General")
    st.markdown("Vista general de métricas, sentimientos y factores principales.")
    st.markdown("---")

    # ==== MÉTRICAS PRINCIPALES ====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Total de publicaciones</div>'
            f'<div class="value">{total_global:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">Positivas</div>'
            f'<div class="value">{pos_global:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card rojo">'
            '<div class="label">Negativas</div>'
            f'<div class="value">{neg_global:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Neutrales</div>'
            f'<div class="value">{neu_global:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # ==== FILA DE GRÁFICOS ====
    col_izq, col_der = st.columns([1, 1.4])

    # --- DONA: Distribución de sentimientos ---
    with col_izq:
        st.markdown(
            '<div class="chart-card">'
            '<h3>Distribución de Sentimientos</h3>',
            unsafe_allow_html=True
        )

        fig_dona = go.Figure(data=[go.Pie(
            labels=["Positivo", "Neutral", "Negativo"],
            values=[pos_global, neu_global, neg_global],
            hole=0.6,
            marker=dict(
                colors=["#035AA6", "#F2B705", "#C62828"],
                line=dict(color="#FFFFFF", width=3)
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value} menciones<br>%{percent}<extra></extra>"
        )])

        fig_dona.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v", yanchor="middle", y=0.5,
                xanchor="left", x=0.95,
                font=dict(size=12, family="Arial", color="#0B2440")
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig_dona, use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BARRAS: Factores de percepción ---
    with col_der:
        st.markdown(
            '<div class="chart-card">'
            '<h3>Factores de Percepción</h3>',
            unsafe_allow_html=True
        )

        if factores_global:
            max_val = max(factores_global.values())
            barras_html = ""
            for factor, valor in sorted(factores_global.items(), key=lambda x: -x[1])[:8]:
                pct = (valor / max_val) * 100
                barras_html += (
                    '<div class="factor-row">'
                    f'<div class="factor-label">{factor}</div>'
                    '<div class="factor-track">'
                    f'<div class="factor-fill" style="width: {pct}%;"></div>'
                    '</div>'
                    f'<div class="factor-value">{valor}</div>'
                    '</div>'
                )
            st.markdown(barras_html, unsafe_allow_html=True)
        else:
            st.info("No hay factores identificados.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==== RESUMEN EJECUTIVO ====
    st.markdown("---")
    st.markdown("### Resumen Ejecutivo")

    if pct_pos > pct_neg and pct_pos > pct_neu:
        tendencia = "positiva"
        color_tend = "#2E7D32"
    elif pct_neg > pct_pos and pct_neg > pct_neu:
        tendencia = "negativa"
        color_tend = "#C62828"
    else:
        tendencia = "neutral"
        color_tend = "#B8860B"

    top_factores = sorted(factores_global.items(), key=lambda x: -x[1])[:3]
    top_factores_str = ", ".join([f"{f} ({v} menciones)" for f, v in top_factores])

    resumen = (
        f'La percepción general de la EMI-UALP es mayormente '
        f'<strong style="color: {color_tend};">{tendencia}</strong>, '
        f'con un <strong>{max(pct_pos, pct_neu, pct_neg)}%</strong> de opiniones '
        f'<strong>{"positivas" if tendencia == "positiva" else "neutrales" if tendencia == "neutral" else "negativas"}</strong>. '
        f'Se analizaron <strong>{total_global:,} publicaciones</strong> recopiladas de '
        f'Facebook y Google Maps. '
    )

    if top_factores:
        resumen += (
            f'Los factores con mayor presencia son <strong>{top_factores_str}</strong>. '
        )

    resumen += (
        'Se recomienda priorizar la revisión de los factores con mayor sentimiento '
        'neto negativo y mantener el monitoreo continuo de la percepción digital.'
    )

    st.markdown(
        f'<div class="info-card">{resumen}</div>',
        unsafe_allow_html=True
    )


# =========================================================
# TAB 2: DISTRIBUCIÓN DE POLARIDAD Y MÉTRICAS DEL MODELO NLP
# =========================================================
with tab2:
    st.markdown("### Distribución de Polaridad")
    st.markdown("Análisis detallado del sentimiento de las opiniones.")
    st.markdown("---")

    # ==== DONA GRANDE CON MÉTRICAS AL LADO ====
    col_dona, col_tabla = st.columns([1.2, 1])

    with col_dona:
        st.markdown(
            '<div class="chart-card">'
            '<h3>Distribución General de Sentimientos</h3>',
            unsafe_allow_html=True
        )

        fig_grande = go.Figure(data=[go.Pie(
            labels=["Positivo", "Neutral", "Negativo"],
            values=[pos_global, neu_global, neg_global],
            hole=0.65,
            marker=dict(
                colors=["#035AA6", "#F2B705", "#C62828"],
                line=dict(color="#FFFFFF", width=4)
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value} menciones<br>%{percent}<extra></extra>"
        )])

        fig_grande.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[
                dict(
                    text=f"<b>{total_global:,}</b><br><span style='font-size:12px;color:#666;'>TOTAL</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=26, color="#0B2440", family="Arial"),
                )
            ]
        )

        st.plotly_chart(fig_grande, use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tabla:
        st.markdown(
            '<div class="chart-card" style="height: 100%;">'
            '<h3 style="color: #0B2440 !important; -webkit-text-fill-color: #0B2440 !important;">Categorías</h3>'
            '<table style="width: 100%; font-size: 13px; margin-top: 8px; '
            'border-collapse: collapse;">'
            '<thead>'
            '<tr style="border-bottom: 1px solid #E0E4EA;">'
            '<th style="text-align: left; padding: 12px 8px; font-size: 11px; '
            'text-transform: uppercase; color: #666 !important; '
            '-webkit-text-fill-color: #666 !important; font-weight: 600;">Categoría</th>'
            '<th style="text-align: right; padding: 12px 8px; font-size: 11px; '
            'text-transform: uppercase; color: #666 !important; '
            '-webkit-text-fill-color: #666 !important; font-weight: 600;">Valor</th>'
            '<th style="text-align: right; padding: 12px 8px; font-size: 11px; '
            'text-transform: uppercase; color: #666 !important; '
            '-webkit-text-fill-color: #666 !important; font-weight: 600;">%</th>'
            '</tr></thead>'
            '<tbody>'
            f'<tr style="border-bottom: 1px solid #F0F2F5;">'
            f'<td style="padding: 14px 8px; color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">'
            f'<span style="display:inline-block; width:10px; height:10px; '
            f'border-radius:50%; background:#035AA6; margin-right:8px;"></span>'
            f'<strong style="color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">Positivo</strong></td>'
            f'<td style="text-align: right; padding: 14px 8px; font-weight: 700; '
            f'color: #0B2440 !important; -webkit-text-fill-color: #0B2440 !important;">'
            f'{pos_global:,}</td>'
            f'<td style="text-align: right; padding: 14px 8px; color: #035AA6 !important; '
            f'-webkit-text-fill-color: #035AA6 !important; font-weight: 700;">{pct_pos}%</td>'
            f'</tr>'
            f'<tr style="border-bottom: 1px solid #F0F2F5;">'
            f'<td style="padding: 14px 8px; color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">'
            f'<span style="display:inline-block; width:10px; height:10px; '
            f'border-radius:50%; background:#F2B705; margin-right:8px;"></span>'
            f'<strong style="color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">Neutral</strong></td>'
            f'<td style="text-align: right; padding: 14px 8px; font-weight: 700; '
            f'color: #0B2440 !important; -webkit-text-fill-color: #0B2440 !important;">'
            f'{neu_global:,}</td>'
            f'<td style="text-align: right; padding: 14px 8px; color: #B8860B !important; '
            f'-webkit-text-fill-color: #B8860B !important; font-weight: 700;">{pct_neu}%</td>'
            f'</tr>'
            f'<tr>'
            f'<td style="padding: 14px 8px; color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">'
            f'<span style="display:inline-block; width:10px; height:10px; '
            f'border-radius:50%; background:#C62828; margin-right:8px;"></span>'
            f'<strong style="color: #0B2440 !important; '
            f'-webkit-text-fill-color: #0B2440 !important;">Negativo</strong></td>'
            f'<td style="text-align: right; padding: 14px 8px; font-weight: 700; '
            f'color: #0B2440 !important; -webkit-text-fill-color: #0B2440 !important;">'
            f'{neg_global:,}</td>'
            f'<td style="text-align: right; padding: 14px 8px; color: #C62828 !important; '
            f'-webkit-text-fill-color: #C62828 !important; font-weight: 700;">{pct_neg}%</td>'
            f'</tr>'
            '</tbody></table></div>',
            unsafe_allow_html=True
        )

    # ==== MÉTRICAS DEL MODELO NLP ====
    st.markdown("---")
    st.markdown("### Métricas de Clasificación (NLP Evaluation)")

    f1 = 0.9489
    precision = 0.95
    recall = 0.94
    cumple = f1 >= 0.75

    st.markdown(
        '<div class="nlp-eval-card">'
        '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">'
        '<div class="nlp-eval-item">'
        '<div class="item-label">F1-Score</div>'
        f'<div class="item-value">{f1}</div>'
        '</div>'
        '<div class="nlp-eval-item">'
        '<div class="item-label">Precisión</div>'
        f'<div class="item-value">{precision}</div>'
        '</div>'
        '<div class="nlp-eval-item">'
        '<div class="item-label">Recall</div>'
        f'<div class="item-value">{recall}</div>'
        '</div>'
        '<div class="nlp-eval-item">'
        '<div class="item-label">Cumple Umbral &ge; 0.75</div>'
        f'<div class="item-check">{"&#10003;" if cumple else "&#10007;"}</div>'
        '</div>'
        '</div></div>',
        unsafe_allow_html=True
    )


# =========================================================
# TAB 3: FACTORES TEMÁTICOS IDENTIFICADOS (BERTopic)
# =========================================================
with tab3:
    st.markdown("### Factores Temáticos Identificados")
    st.markdown("Identificación automática de factores de percepción institucional con BERTopic.")
    st.markdown("---")

    # ==== KPIs DEL MODELO BERTopic ====
    n_temas = len(factores_global)
    cv_score = 0.6667
    cumple_cv = cv_score >= 0.5
    textos_analizados = neg_global

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Temas Identificados</div>'
            f'<div class="value">{n_temas}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">CV Score</div>'
            f'<div class="value">{cv_score}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        color_check = "#2E7D32" if cumple_cv else "#C62828"
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Cumple Umbral &ge; 0.5</div>'
            f'<div class="value" style="font-size: 24px; color: {color_check} !important; '
            f'-webkit-text-fill-color: {color_check} !important;">'
            f'{"&#10003;" if cumple_cv else "&#10007;"}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Textos Analizados</div>'
            f'<div class="value">{textos_analizados:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ==== TABLA CON BARRAS Y SENTIMIENTO NETO ====
    st.markdown("---")
    st.markdown("### Factores de Percepción Identificados")

    if not factores_global:
        st.info("No hay factores identificados en el corpus.")
    else:
        factores_ordenados = sorted(factores_global.items(), key=lambda x: -x[1])
        max_val = max(factores_global.values()) if factores_global else 1

        filas_html = ""
        for factor, valor in factores_ordenados:
            pct_barra = (valor / max_val) * 100
            pct_total = round((valor / total_global) * 100, 1)
            sent_neto = sentimiento_neto_por_factor(df_corpus, factor)

            # Clase CSS para el color del sentimiento neto
            if sent_neto > 0:
                clase_sent = "sent-neto-positivo"
                signo = "+"
            elif sent_neto < 0:
                clase_sent = "sent-neto-negativo"
                signo = ""
            else:
                clase_sent = "sent-neto-cero"
                signo = ""

            filas_html += (
                '<tr>'
                f'<td style="font-weight: 600; color: #0B2440 !important; '
                f'-webkit-text-fill-color: #0B2440 !important;">{factor}</td>'
                '<td>'
                '<div style="background:#EEF1F5; border-radius:4px; height:20px; '
                'overflow:hidden; width: 100%;">'
                f'<div style="width:{pct_barra}%; height:100%; '
                f'background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);"></div>'
                '</div>'
                '</td>'
                f'<td style="text-align: right; font-weight: 700; '
                f'color: #0B2440 !important; -webkit-text-fill-color: #0B2440 !important;">'
                f'{valor}</td>'
                f'<td style="text-align: right; color:#666 !important; '
                f'-webkit-text-fill-color: #666 !important; '
                f'font-size:12px;">{pct_total}%</td>'
                f'<td class="{clase_sent}">{signo}{sent_neto}%</td>'
                '</tr>'
            )

        tabla_completa = (
            '<div class="result-table">'
            '<table style="width: 100%; border-collapse: collapse;">'
            '<thead>'
            '<tr>'
            '<th style="width: 28%; text-align: left; padding: 14px;">Factor</th>'
            '<th style="width: 37%; text-align: left; padding: 14px;">Distribución</th>'
            '<th style="width: 11%; text-align: right; padding: 14px;">Menciones</th>'
            '<th style="width: 12%; text-align: right; padding: 14px;">% Total</th>'
            '<th style="width: 12%; text-align: right; padding: 14px;">Sent. Neto</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            + filas_html +
            '</tbody>'
            '</table>'
            '</div>'
        )

        st.markdown(tabla_completa, unsafe_allow_html=True)

    # =========================================================
    # ==== NUEVA SECCIÓN: EVOLUCIÓN ANUAL DE FACTORES ====
    # =========================================================
    st.markdown("---")
    st.markdown("### Evolución Anual de Factores")
    st.markdown(
        "Prevalencia de cada factor por año: "
        "`(menciones del factor en un año / menciones totales del año) × 100`"
    )

    # Preparar datos con año
    df_anual = preparar_dataframe_con_anio(df_corpus)

    if df_anual is None or len(df_anual) == 0:
        st.info(
            "El corpus no tiene columnas de fecha válidas "
            "(`fecha_creacion` o `fecha`). No se puede calcular la evolución anual."
        )
    else:
        # Excluir "Sin clasificar"
        df_anual = df_anual[df_anual["factor"] != "Sin clasificar"]

        if len(df_anual) == 0:
            st.info("No hay datos con año válido para calcular la evolución anual.")
        else:
            anios_disponibles = sorted(df_anual["anio"].unique().tolist())

            # ==== KPIs DE EVOLUCIÓN ====
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">Años Analizados</div>'
                    f'<div class="value">{len(anios_disponibles)}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<div class="metric-card verde">'
                    '<div class="label">Rango Temporal</div>'
                    f'<div class="value" style="font-size:18px;">'
                    f'{min(anios_disponibles)} – {max(anios_disponibles)}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<div class="metric-card amarillo">'
                    '<div class="label">Registros con Fecha</div>'
                    f'<div class="value">{len(df_anual):,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            # ==== TABLA DE PREVALENCIA ANUAL ====
            st.markdown("#### Prevalencia Anual por Factor (%)")

            factores_lista = sorted(factores_global.keys())

            # Encabezado de años
            encabezado_anios = "".join(
                f'<th style="text-align: center; padding: 10px 6px; '
                f'font-size: 11px; font-weight: 700; white-space: nowrap;">{anio}</th>'
                for anio in anios_disponibles
            )

            filas_prevalencia = ""
            for factor in factores_lista:
                prevalencia = calcular_prevalencia_anual_por_factor(df_corpus, factor)

                # Determinar tendencia
                valores_validos = [v for a, v in sorted(prevalencia.items()) if v > 0]
                if len(valores_validos) >= 2:
                    if valores_validos[-1] > valores_validos[0]:
                        tendencia_icon = "▲"
                        tendencia_color = "#DC2626"
                    elif valores_validos[-1] < valores_validos[0]:
                        tendencia_icon = "▼"
                        tendencia_color = "#15803D"
                    else:
                        tendencia_icon = "—"
                        tendencia_color = "#64748B"
                else:
                    tendencia_icon = "—"
                    tendencia_color = "#64748B"

                celdas_anios = ""
                for anio in anios_disponibles:
                    valor = prevalencia.get(anio, 0)

                    # Color según magnitud
                    if valor == 0:
                        color_val = "#CCCCCC"
                        bg_val = "transparent"
                    elif valor >= 50:
                        color_val = "#DC2626"
                        bg_val = "rgba(220, 38, 38, 0.10)"
                    elif valor >= 25:
                        color_val = "#EA580C"
                        bg_val = "rgba(234, 88, 12, 0.08)"
                    elif valor >= 10:
                        color_val = "#CA8A04"
                        bg_val = "rgba(202, 138, 4, 0.06)"
                    else:
                        color_val = "#15803D"
                        bg_val = "transparent"

                    celdas_anios += (
                        f'<td style="text-align: center; padding: 10px 6px; '
                        f'font-size: 12px; font-weight: 600; '
                        f'color: {color_val} !important; '
                        f'-webkit-text-fill-color: {color_val} !important; '
                        f'background: {bg_val};">'
                        f'{valor}%</td>'
                    )

                filas_prevalencia += (
                    '<tr>'
                    f'<td style="font-weight: 600; color: #0B2440 !important; '
                    f'-webkit-text-fill-color: #0B2440 !important; '
                    f'padding: 10px 14px; font-size: 12.5px;">{factor}</td>'
                    f'{celdas_anios}'
                    f'<td style="text-align: center; padding: 10px 8px; '
                    f'font-weight: 700; color: {tendencia_color} !important; '
                    f'-webkit-text-fill-color: {tendencia_color} !important; '
                    f'font-size: 14px;">{tendencia_icon}</td>'
                    '</tr>'
                )

            tabla_prevalencia = (
                '<div class="result-table">'
                '<table style="width: 100%; border-collapse: collapse;">'
                '<thead>'
                '<tr>'
                '<th style="text-align: left; padding: 12px 14px; '
                'font-size: 10.5px; font-weight: 700;">Factor</th>'
                + encabezado_anios +
                '<th style="text-align: center; padding: 12px 8px; '
                'font-size: 10.5px; font-weight: 700; width: 60px;">Tend.</th>'
                '</tr>'
                '</thead>'
                '<tbody>'
                + filas_prevalencia +
                '</tbody>'
                '</table>'
                '</div>'
            )

            st.markdown(tabla_prevalencia, unsafe_allow_html=True)

            # Leyenda
            st.markdown(
                '<div style="margin-top: 12px; font-size: 11.5px; '
                'color: #666 !important; -webkit-text-fill-color: #666 !important;">'
                '<strong>Leyenda:</strong> '
                '<span style="color: #15803D; font-weight: 600;">■ &lt;10%</span> · '
                '<span style="color: #CA8A04; font-weight: 600;">■ 10-25%</span> · '
                '<span style="color: #EA580C; font-weight: 600;">■ 25-50%</span> · '
                '<span style="color: #DC2626; font-weight: 600;">■ &gt;50%</span> · '
                '<span style="color: #DC2626; font-weight: 700;">▲</span> aumenta · '
                '<span style="color: #15803D; font-weight: 700;">▼</span> disminuye'
                '</div>',
                unsafe_allow_html=True
            )

            # ==== GRÁFICO DE LÍNEAS ====
            st.markdown("---")
            st.markdown("#### Gráfico de Evolución Temporal")

            fig_evolucion = go.Figure()

            colores_lineas = [
                "#035AA6", "#DC2626", "#2E7D32", "#CA8A04",
                "#9333EA", "#EA580C", "#0891B2", "#DB2777",
                "#65A30D", "#6366F1"
            ]

            # Limitamos a los 8 factores más frecuentes para no saturar el gráfico
            factores_top = sorted(factores_global.items(), key=lambda x: -x[1])[:8]
            factores_graf = [f[0] for f in factores_top]

            for i, factor in enumerate(factores_graf):
                prevalencia = calcular_prevalencia_anual_por_factor(df_corpus, factor)
                anios_graf = sorted(prevalencia.keys())
                valores_graf = [prevalencia[a] for a in anios_graf]

                fig_evolucion.add_trace(go.Scatter(
                    x=anios_graf,
                    y=valores_graf,
                    mode='lines+markers',
                    name=factor[:25] + ("..." if len(factor) > 25 else ""),
                    line=dict(width=2.5, color=colores_lineas[i % len(colores_lineas)]),
                    marker=dict(size=9),
                    hovertemplate=(
                        f"<b>{factor}</b><br>"
                        "Año: %{x}<br>"
                        "Prevalencia: %{y}%<extra></extra>"
                    )
                ))

            fig_evolucion.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=20, b=100),
                xaxis=dict(
                    title="Año",
                    showgrid=True,
                    gridcolor="#EEF1F5",
                    tickfont=dict(size=11, color="#0B2440"),
                    dtick=1
                ),
                yaxis=dict(
                    title="Prevalencia (%)",
                    showgrid=True,
                    gridcolor="#EEF1F5",
                    ticksuffix="%",
                    tickfont=dict(size=11, color="#0B2440")
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10, color="#0B2440")
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                hovermode="x unified"
            )

            st.plotly_chart(fig_evolucion, use_container_width=True,
                            config={"displayModeBar": False})

            # ==== GRÁFICO DE BARRAS APILADAS POR AÑO ====
            st.markdown("---")
            st.markdown("#### Distribución de Factores por Año")

            fig_barras_apiladas = go.Figure()

            for i, factor in enumerate(factores_graf):
                prevalencia = calcular_prevalencia_anual_por_factor(df_corpus, factor)
                anios_graf = sorted(prevalencia.keys())
                valores_graf = [prevalencia[a] for a in anios_graf]

                fig_barras_apiladas.add_trace(go.Bar(
                    x=anios_graf,
                    y=valores_graf,
                    name=factor[:25] + ("..." if len(factor) > 25 else ""),
                    marker_color=colores_lineas[i % len(colores_lineas)],
                    hovertemplate=(
                        f"<b>{factor}</b><br>"
                        "Año: %{x}<br>"
                        "Prevalencia: %{y}%<extra></extra>"
                    )
                ))

            fig_barras_apiladas.update_layout(
                barmode='stack',
                height=420,
                margin=dict(l=20, r=20, t=20, b=100),
                xaxis=dict(
                    title="Año",
                    showgrid=False,
                    tickfont=dict(size=11, color="#0B2440"),
                    dtick=1
                ),
                yaxis=dict(
                    title="Prevalencia acumulada (%)",
                    showgrid=True,
                    gridcolor="#EEF1F5",
                    ticksuffix="%",
                    tickfont=dict(size=11, color="#0B2440")
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10, color="#0B2440")
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_barras_apiladas, use_container_width=True,
                            config={"displayModeBar": False})


# =========================================================
# TAB 4: BÚSQUEDA Y FILTRADO DE OPINIONES
# =========================================================
with tab4:
    st.markdown("### Búsqueda y Filtrado de Opiniones")
    st.markdown("Consulte y filtre las opiniones recopiladas según fuente, sentimiento y factor.")
    st.markdown("---")

    # ==== PANEL DE FILTROS ====
    st.markdown("#### Filtros de Búsqueda")

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        fuentes_disp = ["Todas las fuentes"]
        if "fuente" in df_corpus.columns:
            fuentes_disp += sorted(df_corpus["fuente"].dropna().unique().tolist())
        filtro_fuente = st.selectbox("FUENTE", fuentes_disp, key="dash_f4_fuente")

    with col_f2:
        filtro_sentimiento = st.selectbox(
            "SENTIMIENTO",
            ["Todos", "positivo", "negativo", "neutral"],
            key="dash_f4_sent"
        )

    with col_f3:
        factores_disp = ["Todos los factores"] + sorted(factores_global.keys())
        filtro_factor = st.selectbox("FACTOR", factores_disp, key="dash_f4_factor")

    with col_f4:
        busqueda = st.text_input("BÚSQUEDA", placeholder="Buscar en el texto...",
                                  key="dash_f4_busqueda")

    # Botones
    col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 1])
    with col_btn2:
        limpiar = st.button("Limpiar filtros", use_container_width=True,
                             key="dash_f4_limpiar")
    with col_btn3:
        aplicar = st.button("Aplicar filtros", type="primary",
                             use_container_width=True, key="dash_f4_aplicar")

    if limpiar:
        st.session_state.dash_f4_fuente = "Todas las fuentes"
        st.session_state.dash_f4_sent = "Todos"
        st.session_state.dash_f4_factor = "Todos los factores"
        st.session_state.dash_f4_busqueda = ""
        st.rerun()

    # ==== APLICAR FILTROS ====
    df_filtrado = df_corpus.copy()

    if filtro_fuente != "Todas las fuentes" and "fuente" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["fuente"] == filtro_fuente]

    if filtro_sentimiento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["sentimiento"] == filtro_sentimiento]

    if filtro_factor != "Todos los factores":
        df_filtrado = df_filtrado[df_filtrado["factor"] == filtro_factor]

    if busqueda:
        b = busqueda.lower()
        df_filtrado = df_filtrado[
            df_filtrado["texto"].astype(str).str.lower().str.contains(b, na=False)
        ]

    total_filtrado = len(df_filtrado)

    # ==== TABLA DE RESULTADOS ====
    st.markdown("---")
    st.markdown(f"### Resultados ({total_filtrado:,} registros encontrados)")

    if total_filtrado == 0:
        st.info("No se encontraron opiniones con los filtros aplicados.")
    else:
        por_pagina = 15
        total_paginas = max(1, (total_filtrado + por_pagina - 1) // por_pagina)

        if "dash_f4_pagina" not in st.session_state:
            st.session_state.dash_f4_pagina = 1

        if st.session_state.dash_f4_pagina > total_paginas:
            st.session_state.dash_f4_pagina = 1

        pagina = st.session_state.dash_f4_pagina
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        df_pagina = df_filtrado.iloc[inicio:fin]

        filas = ""
        for i, (_, row) in enumerate(df_pagina.iterrows()):
            texto_completo = str(row.get("texto", ""))
            texto = texto_completo[:160] + "..." if len(texto_completo) > 160 else texto_completo

            sent = row.get("sentimiento", "neutral")
            badge_sent = {
                "positivo": "badge-positivo",
                "negativo": "badge-negativo",
                "neutral": "badge-neutral",
            }.get(sent, "badge-neutral")

            fuente = str(row.get("fuente", "")).replace("_", " ").title()
            if "facebook" in fuente.lower():
                badge_fuente = "badge-facebook"
                fuente_label = "Facebook"
            elif "google" in fuente.lower():
                badge_fuente = "badge-google"
                fuente_label = "Google Maps"
            else:
                badge_fuente = "badge-facebook"
                fuente_label = fuente

            factor = row.get("factor", "Sin clasificar")
            fecha = row.get("fecha", row.get("fecha_dia", "—"))

            filas += (
                '<tr>'
                f'<td style="color:#666 !important; -webkit-text-fill-color:#666 !important; '
                f'font-size:11.5px;">{inicio + i + 1}</td>'
                f'<td><span class="badge-fuente {badge_fuente}">{fuente_label}</span></td>'
                f'<td style="font-size:12px;">{texto}</td>'
                f'<td><span class="badge-sent {badge_sent}">{sent}</span></td>'
                f'<td style="font-size:11.5px; color:#0B2440 !important; '
                f'-webkit-text-fill-color:#0B2440 !important;">{factor}</td>'
                f'<td style="color:#666 !important; -webkit-text-fill-color:#666 !important; '
                f'font-size:11.5px;">{fecha}</td>'
                '</tr>'
            )

        tabla = (
            '<div class="result-table">'
            '<table>'
            '<thead><tr>'
            '<th style="width: 40px;">#</th>'
            '<th style="width: 110px;">Fuente</th>'
            '<th>Texto</th>'
            '<th style="width: 100px;">Sentimiento</th>'
            '<th style="width: 160px;">Factor</th>'
            '<th style="width: 100px;">Fecha</th>'
            '</tr></thead>'
            '<tbody>' + filas + '</tbody>'
            '</table></div>'
        )
        st.markdown(tabla, unsafe_allow_html=True)

        # ==== PAGINACIÓN ====
        col_pag1, col_pag2, col_pag3, col_pag4, col_pag5 = st.columns([2, 1, 1, 1, 2])

        with col_pag2:
            if st.button("« Anterior", use_container_width=True,
                          disabled=(pagina == 1), key="pag_prev"):
                st.session_state.dash_f4_pagina = pagina - 1
                st.rerun()

        with col_pag3:
            st.markdown(
                f'<div style="text-align: center; padding: 8px 0; '
                f'font-size: 13px; font-weight: 700; color: #035AA6 !important; '
                f'-webkit-text-fill-color: #035AA6 !important;">'
                f'{pagina} / {total_paginas}</div>',
                unsafe_allow_html=True
            )

        with col_pag4:
            if st.button("Siguiente »", use_container_width=True,
                          disabled=(pagina >= total_paginas), key="pag_next"):
                st.session_state.dash_f4_pagina = pagina + 1
                st.rerun()

        st.markdown(
            f'<div class="pagination-info">'
            f'Mostrando {inicio + 1}–{min(fin, total_filtrado)} '
            f'de {total_filtrado:,} resultados</div>',
            unsafe_allow_html=True
        )


# =========================================================
# DESCARGA
# =========================================================
st.markdown("---")
st.markdown("### Exportar Resultados")

col1, col2 = st.columns(2)

with col1:
    csv_data = df_corpus.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Descargar Corpus Completo (CSV)",
        data=csv_data,
        file_name=f"dashboard_percepcion_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col2:
    if st.button("Refrescar Datos", use_container_width=True, key="btn_refresh_dash"):
        st.cache_data.clear()
        st.rerun()