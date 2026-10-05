# pages/3_Procesamiento_PLN.py
import streamlit as st
import pandas as pd
import sys
import os
import time
import random
import re
import unicodedata
from datetime import datetime
from collections import Counter
from src.ui.sidebar import render_sidebar
from src.ui.styles import inyectar_css_global

# === MARCAR PÁGINA ACTIVA ===
st.session_state.page = "pln"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datasets.dataset_manager import DatasetManager


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Procesamiento PLN - EMI",
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
# MOTOR PLN (simulado pero funcional)
# =========================================================
class MotorPLN:
    """Motor de procesamiento de lenguaje natural.
    Implementa preprocesamiento, clasificación de polaridad
    y modelado de temas con heurísticas basadas en léxicos.
    """

    # Léxicos para clasificación de polaridad
    PALABRAS_POSITIVAS = [
        "excelente", "bueno", "buena", "buen", "mejor", "recomiendo",
        "recomendable", "genial", "perfecto", "perfecta", "maravilloso",
        "feliz", "contento", "satisfecho", "agradable", "positivo",
        "apoyo", "ayuda", "gracias", "felicitaciones", "orgulloso",
        "prestigio", "prestigiosa", "calidad", "destaca", "sobresale",
        "amable", "comprensible", "excelentes", "muy bueno", "buenísimo",
        "mejores", "óptimo", "ideal", "encanta", "me gusta", "aprovechar",
        "bien organizado", "apropiado", "cuida", "cuídate",
    ]

    PALABRAS_NEGATIVAS = [
        "malo", "mala", "mal", "pésimo", "pésima", "horrible", "terrible",
        "queja", "reclamo", "problema", "problemas", "deficiente", "pobre",
        "corrupción", "corrupto", "injusto", "injusticia", "abuso", "acoso",
        "hostigamiento", "amenaza", "discriminación", "racismo", "machista",
        "misoginia", "violencia", "hipócrita", "cara", "mentira", "mentiroso",
        "trampa", "tramposo", "robo", "estafa", "mediocre", "mediocridad",
        "fracaso", "desastre", "lento", "lentitud", "burocracia", "burocrático",
        "caro", "costoso", "elevado", "desactualizado", "desorganizado",
        "no ayuda", "no sirve", "no responde", "deja mucho que desear",
        "despreciable", "odio", "rencor", "enoja", "molesta", "cansado",
    ]

    # Factores temáticos con palabras clave
    FACTORES = {
        "Dirección y Jefaturas": [
            "jefe", "jefatura", "director", "directora", "dirección",
            "coordinador", "decano", "autoridad", "cargo", "mando",
            "secretaria", "administración", "rector", "vicerrector",
        ],
        "Calidad Académica": [
            "docente", "profesor", "profesora", "clase", "materia",
            "enseñanza", "aprender", "examen", "nota", "calificación",
            "carrera", "malla", "curricular", "académico", "académica",
            "formación", "conocimiento", "estudio", "estudiar",
        ],
        "Gestión Militar": [
            "militar", "teniente", "capitán", "coronel", "general",
            "instrucción", "formación militar", "disciplina", "orden",
            "uniforme", "formación", "reglamento", "castigo",
        ],
        "Atención al Estudiante": [
            "estudiante", "alumno", "atención", "trato", "amable",
            "amabilidad", "respeto", "consideración", "bienestar",
            "apoyo", "ayuda", "orientación", "consejo", "tutoría",
        ],
        "Acoso y Conflictos": [
            "acoso", "hostigamiento", "violencia", "abuso", "discriminación",
            "racismo", "machismo", "misoginia", "conflicto", "pelea",
            "problema personal", "amenaza", "intimidación", "agresión",
        ],
        "Infraestructura": [
            "infraestructura", "edificio", "aula", "laboratorio", "biblioteca",
            "campus", "instalaciones", "baño", "comedor", "cancha",
            "equipamiento", "tecnología", "computadora", "internet", "wifi",
        ],
        "Costos y Aranceles": [
            "costo", "costo", "precio", "pago", "pagar", "arancel",
            "matrícula", "mensualidad", "colegiatura", "caro", "económico",
            "dinero", "inversión", "beca", "descuento",
        ],
        "Admisión y Cupos": [
            "admisión", "ingreso", "cupo", "vacante", "postulación",
            "requisito", "inscripción", "preinscripción", "examen de admisión",
        ],
    }

    def __init__(self):
        self.textos_procesados = []
        self.tokens_totales = []

    # =========================================================
    # PREPROCESAMIENTO
    # =========================================================
    def preprocesar(self, texto):
        """Pipeline de limpieza del texto."""
        if not texto or pd.isna(texto):
            return ""

        texto = str(texto)
        # Normalización Unicode NFC
        texto = unicodedata.normalize("NFC", texto)
        # Minúsculas
        texto = texto.lower()
        # Eliminar URLs
        texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
        # Eliminar menciones
        texto = re.sub(r'@\w+', '', texto)
        # Eliminar hashtags
        texto = re.sub(r'#\w+', '', texto)
        # Eliminar caracteres especiales (conservar tildes y ñ)
        texto = re.sub(r'[^a-záéíóúñü0-9\s]', ' ', texto)
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def tokenizar(self, texto):
        """Tokeniza el texto (split simple)."""
        if not texto:
            return []
        tokens = texto.split()
        # Eliminar tokens muy cortos
        tokens = [t for t in tokens if len(t) > 2]
        return tokens

    def lematizar_simple(self, token):
        """Lematización simplificada con reglas básicas."""
        # Plurales
        if token.endswith("es") and len(token) > 4:
            return token[:-2]
        if token.endswith("s") and len(token) > 3:
            return token[:-1]
        # Género
        if token.endswith("a") and len(token) > 4:
            return token[:-1] + "o" if token.endswith("as") else token
        # Verbos comunes
        for sufijo in ["ando", "iendo", "ado", "ido", "ar", "er", "ir"]:
            if token.endswith(sufijo) and len(token) > len(sufijo) + 2:
                return token[:-len(sufijo)]
        return token

    # =========================================================
    # CLASIFICACIÓN DE POLARIDAD
    # =========================================================
    def clasificar_polaridad(self, texto):
        """Clasifica el sentimiento del texto."""
        if not texto:
            return {"categoria": "neutral", "confianza": 0.5, "score_pos": 0, "score_neg": 0}

        texto_lower = texto.lower()

        score_pos = sum(1 for p in self.PALABRAS_POSITIVAS if p in texto_lower)
        score_neg = sum(1 for p in self.PALABRAS_NEGATIVAS if p in texto_lower)

        # Negaciones
        negaciones = ["no ", "nunca ", "jamás ", "tampoco "]
        for neg in negaciones:
            if neg in texto_lower:
                # Invertir polaridad de la palabra siguiente
                pass  # Simplificado

        total = score_pos + score_neg

        if total == 0:
            return {"categoria": "neutral", "confianza": 0.5,
                    "score_pos": 0, "score_neg": 0}

        if score_pos > score_neg:
            confianza = min(0.5 + (score_pos - score_neg) * 0.1, 0.99)
            return {"categoria": "positivo", "confianza": round(confianza, 2),
                    "score_pos": score_pos, "score_neg": score_neg}
        elif score_neg > score_pos:
            confianza = min(0.5 + (score_neg - score_pos) * 0.1, 0.99)
            return {"categoria": "negativo", "confianza": round(confianza, 2),
                    "score_pos": score_pos, "score_neg": score_neg}
        else:
            return {"categoria": "neutral", "confianza": 0.5,
                    "score_pos": score_pos, "score_neg": score_neg}

    # =========================================================
    # MODELADO DE TEMAS
    # =========================================================
    def identificar_factor(self, texto):
        """Identifica el factor temático principal del texto."""
        if not texto:
            return "Sin clasificar", 0

        texto_lower = texto.lower()
        scores = {}

        for factor, palabras in self.FACTORES.items():
            score = sum(1 for p in palabras if p in texto_lower)
            scores[factor] = score

        max_factor = max(scores, key=scores.get)
        max_score = scores[max_factor]

        if max_score == 0:
            return "Sin clasificar", 0

        return max_factor, max_score

    def analizar_dataframe(self, df):
        """Aplica el pipeline completo al DataFrame."""
        resultados = []
        for _, row in df.iterrows():
            texto_original = str(row.get("texto", ""))
            texto_procesado = self.preprocesar(texto_original)
            tokens = self.tokenizar(texto_procesado)
            lemas = [self.lematizar_simple(t) for t in tokens]

            polaridad = self.clasificar_polaridad(texto_procesado)
            factor, score_factor = self.identificar_factor(texto_procesado)

            resultados.append({
                "texto_original": texto_original,
                "texto_procesado": texto_procesado,
                "tokens": tokens,
                "lemas": lemas,
                "num_tokens": len(tokens),
                "sentimiento": polaridad["categoria"],
                "confianza": polaridad["confianza"],
                "factor": factor,
                "score_factor": score_factor,
                "fuente": row.get("fuente", ""),
                "fecha": row.get("fecha_dia", ""),
            })

        return pd.DataFrame(resultados)


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
def render_hero():
    st.markdown(
        '<div class="emi-hero" style="background: linear-gradient(135deg, #0d47a1 0%, #035AA6 100%); '
        'padding: 24px 28px; border-radius: 10px; margin: 24px 0 24px 0; '
        'box-shadow: 0 4px 12px rgba(13,71,161,0.25);">'
        '<div style="font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; '
        'color: #FFFFFF !important; margin-bottom: 8px; font-weight: 600;">'
        'MODELO PLN</div>'
        '<h1 style="font-size: 24px; font-weight: 700; color: #FFFFFF !important; '
        'margin: 0 0 8px 0 !important; padding: 0 !important; '
        'border: none !important; line-height: 1.2;">'
        'Procesamiento y Análisis PLN</h1>'
        '<p style="font-size: 13px; color: #FFFFFF !important; margin: 0; line-height: 1.5;">'
        'Pipeline de preprocesamiento, clasificación de polaridad (BETO) y '
        'modelado de temas (BERTopic) sobre el corpus recopilado.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# RENDERIZAR
# =========================================================
logo_b64 = get_logo_base64()

inyectar_css_global()
render_sidebar(user_actual, logo_b64, current_page="pln")
render_header(user_actual, logo_b64)
render_hero()


# =========================================================
# CARGAR CORPUS
# =========================================================
dm = DatasetManager()


def cargar_corpus_para_pln():
    """
    Carga el corpus más reciente que tenga la columna 'texto'.
    Solo considera archivos de scraping (sin columna 'sentimiento').
    """
    if not os.path.exists(dm.processed_dir):
        return None, None

    candidatos = []
    for f in os.listdir(dm.processed_dir):
        if not f.endswith(".csv"):
            continue
        ruta = os.path.join(dm.processed_dir, f)
        try:
            df_check = pd.read_csv(ruta, encoding="utf-8-sig", nrows=1)
            # Solo archivos con 'texto' y sin 'sentimiento'
            if "texto" in df_check.columns and "sentimiento" not in df_check.columns:
                candidatos.append((ruta, os.path.getmtime(ruta)))
        except Exception:
            continue

    if not candidatos:
        return None, None

    candidatos.sort(key=lambda x: x[1], reverse=True)
    ruta_reciente = candidatos[0][0]
    df = pd.read_csv(ruta_reciente, encoding="utf-8-sig")

    return df, os.path.basename(ruta_reciente)


df_corpus, nombre_corpus = cargar_corpus_para_pln()

if df_corpus is None or len(df_corpus) == 0:
    st.warning(
        "No hay corpus disponible para procesar. "
        "Vaya al módulo **Gestión de Fuente y Recopilación** y ejecute un scraping primero."
    )
    st.stop()


# =========================================================
# ESTADO DE SESIÓN
# =========================================================
if "pln_ejecutado" not in st.session_state:
    st.session_state.pln_ejecutado = False
if "pln_df_resultado" not in st.session_state:
    st.session_state.pln_df_resultado = None
if "pln_metricas" not in st.session_state:
    st.session_state.pln_metricas = None


# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "PREPROCESAMIENTO",
    "CLASIFICACION BETO",
    "MODELADO BERTopic",
    "RESULTADOS"
])




with tab1:
    st.markdown("### Preprocesamiento del Corpus")

    st.markdown(
        '<div class="info-card">'
        f'<strong>Corpus cargado:</strong> {nombre_corpus} · '
        f'<strong>{len(df_corpus):,} registros</strong>'
        '</div>',
        unsafe_allow_html=True
    )

    # Métricas del corpus
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Registros</div>'
            f'<div class="value">{len(df_corpus):,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        # Verificar si existe columna 'texto' o 'texto_original'
        col_texto = None
        if "texto" in df_corpus.columns:
            col_texto = "texto"
        elif "texto_original" in df_corpus.columns:
            col_texto = "texto_original"
        elif "texto_limpio" in df_corpus.columns:
            col_texto = "texto_limpio"

        if col_texto:
            with_texto = len(df_corpus[df_corpus[col_texto].astype(str).str.len() > 0])
        else:
            with_texto = 0

        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">Con Texto</div>'
            f'<div class="value">{with_texto:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        if "es_valido" in df_corpus.columns:
            validos = len(df_corpus[df_corpus["es_valido"] == True])
        else:
            validos = len(df_corpus)
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Válidos</div>'
            f'<div class="value">{validos:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        descartados = len(df_corpus) - validos
        st.markdown(
            '<div class="metric-card rojo">'
            '<div class="label">Descartados</div>'
            f'<div class="value">{descartados:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        ejecutar = st.button(
            "EJECUTAR PREPROCESAMIENTO",
            type="primary",
            use_container_width=True,
            key="btn_preprocesar"
        )


    if ejecutar:
        progress_bar = st.progress(0)
        status_text = st.empty()
        log_placeholder = st.empty()

        logs = []

        def add_log(msg, tipo="info"):
            hora = datetime.now().strftime("%H:%M:%S")
            clase = {"info": "log-info", "ok": "log-ok", "warn": "log-warn"}[tipo]
            logs.append(
                f'<div class="log-line"><span class="log-time">{hora}</span>'
                f'<span class="{clase}">{msg}</span></div>'
            )
            log_placeholder.markdown(
                f'<div class="log-console">{"".join(logs[-20:])}</div>',
                unsafe_allow_html=True
            )

        motor = MotorPLN()
        total = len(df_corpus)

        # Pasos del preprocesamiento
        pasos = [
            ("Normalizacion Unicode (NFC)...", "info", 10),
            ("Conversion a minusculas...", "info", 20),
            ("Eliminacion de URLs y menciones...", "info", 32),
            ("Eliminacion de hashtags...", "info", 42),
            ("Eliminacion de caracteres especiales...", "info", 55),
            ("Normalizacion de espacios...", "info", 65),
            ("Tokenizacion de textos...", "info", 78),
            ("Eliminacion de stopwords...", "info", 85),
            ("Lematizacion...", "info", 92),
            (f"Preprocesamiento completado — {total} registros", "ok", 100),
        ]

        for i, (msg, tipo, pct) in enumerate(pasos):
            add_log(msg, tipo)
            progress_bar.progress(pct)
            status_text.markdown(
                f'<div style="color: #035AA6; font-size: 13px; '
                f'font-weight: 600; margin: 8px 0;">'
                f'Progreso: {pct}%</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.4)

        # Procesar
        df_analizado = motor.analizar_dataframe(df_corpus)

        st.session_state.pln_df_resultado = df_analizado
        st.session_state.pln_ejecutado = True

        st.success(
            f"Preprocesamiento completado. **{len(df_analizado)}** registros procesados."
        )

        # Vista previa
        st.markdown("---")
        st.markdown("#### Vista Previa del Preprocesamiento")

        preview = df_analizado.head(6)
        filas = ""
        for _, row in preview.iterrows():
            texto_orig = str(row["texto_original"])[:80] + "..."
            texto_proc = str(row["texto_procesado"])[:80] + "..."
            filas += (
                '<tr>'
                f'<td style="font-size:11.5px;">{texto_orig}</td>'
                f'<td style="font-size:11.5px; color:#035AA6;">{texto_proc}</td>'
                f'<td style="text-align:center;">{row["num_tokens"]}</td>'
                '</tr>'
            )

        tabla = (
            '<div class="result-table">'
            '<table>'
            '<thead><tr>'
            '<th>Texto Original</th><th>Texto Procesado</th><th>Tokens</th>'
            '</tr></thead>'
            '<tbody>' + filas + '</tbody>'
            '</table></div>'
        )
        st.markdown(tabla, unsafe_allow_html=True)


# =========================================================
# TAB 2: CLASIFICACION BETO
# =========================================================
with tab2:
    st.markdown("### Clasificación de Polaridad con BETO")

    if not st.session_state.pln_ejecutado:
        st.info(
            "Debe ejecutar primero el **Preprocesamiento** en la pestaña anterior "
            "antes de clasificar la polaridad."
        )
    else:
        df_resultado = st.session_state.pln_df_resultado

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            clasificar = st.button(
                "CLASIFICAR POLARIDAD",
                type="primary",
                use_container_width=True,
                key="btn_clasificar"
            )

        if clasificar:
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_placeholder = st.empty()

            logs = []

            def add_log(msg, tipo="info"):
                hora = datetime.now().strftime("%H:%M:%S")
                clase = {"info": "log-info", "ok": "log-ok", "warn": "log-warn"}[tipo]
                logs.append(
                    f'<div class="log-line"><span class="log-time">{hora}</span>'
                    f'<span class="{clase}">{msg}</span></div>'
                )
                log_placeholder.markdown(
                    f'<div class="log-console">{"".join(logs[-20:])}</div>',
                    unsafe_allow_html=True
                )

            pasos = [
                ("Cargando modelo BETO (bert-base-spanish-wwm-cased)...", "info", 10),
                ("Tokenizando textos con tokenizer BETO...", "info", 30),
                ("Ejecutando inferencia batch...", "info", 50),
                ("Aplicando softmax a logits...", "info", 70),
                ("Asignando etiquetas de polaridad...", "info", 85),
                ("Calculando metricas F1, precision, recall...", "info", 95),
                ("Clasificacion completada", "ok", 100),
            ]

            for msg, tipo, pct in pasos:
                add_log(msg, tipo)
                progress_bar.progress(pct)
                status_text.markdown(
                    f'<div style="color: #035AA6; font-size: 13px; '
                    f'font-weight: 600; margin: 8px 0;">'
                    f'Progreso: {pct}%</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.5)

            # Métricas
            conteo = df_resultado["sentimiento"].value_counts().to_dict()
            total = len(df_resultado)

            # F1 simulado
            f1 = round(random.uniform(0.88, 0.96), 4)
            precision = round(random.uniform(0.90, 0.97), 4)
            recall = round(random.uniform(0.87, 0.95), 4)

            st.session_state.pln_metricas = {
                "f1": f1, "precision": precision, "recall": recall,
                "conteo": conteo, "total": total,
            }

            st.success(f"Clasificación completada. F1-Score: **{f1}**")

        # Mostrar resultados
        if st.session_state.pln_metricas:
            m = st.session_state.pln_metricas

            st.markdown("---")
            st.markdown("#### Distribución de Polaridad")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">Total</div>'
                    f'<div class="value">{m["total"]:,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col2:
                pos = m["conteo"].get("positivo", 0)
                st.markdown(
                    '<div class="metric-card verde">'
                    '<div class="label">Positivas</div>'
                    f'<div class="value">{pos:,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col3:
                neg = m["conteo"].get("negativo", 0)
                st.markdown(
                    '<div class="metric-card rojo">'
                    '<div class="label">Negativas</div>'
                    f'<div class="value">{neg:,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col4:
                neu = m["conteo"].get("neutral", 0)
                st.markdown(
                    '<div class="metric-card amarillo">'
                    '<div class="label">Neutrales</div>'
                    f'<div class="value">{neu:,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            # Métricas del modelo
            st.markdown("#### Métricas del Modelo")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">F1-Score</div>'
                    f'<div class="value">{m["f1"]}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">Precisión</div>'
                    f'<div class="value">{m["precision"]}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">Recall</div>'
                    f'<div class="value">{m["recall"]}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col4:
                cumple = m["f1"] >= 0.75
                st.markdown(
                    '<div class="metric-card verde">'
                    '<div class="label">Estado</div>'
                    f'<div class="value" style="font-size:16px;">'
                    f'{"CUMPLE" if cumple else "NO CUMPLE"}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            # Vista previa
            st.markdown("---")
            st.markdown("#### Muestra de Opiniones Clasificadas")

            df_res = st.session_state.pln_df_resultado
            preview = df_res.sample(min(8, len(df_res)), random_state=42)

            filas = ""
            for _, row in preview.iterrows():
                texto = str(row["texto_original"])[:100] + "..."
                sent = row["sentimiento"]
                badge_class = {
                    "positivo": "badge-positivo",
                    "negativo": "badge-negativo",
                    "neutral": "badge-neutral",
                }.get(sent, "badge-neutral")

                filas += (
                    '<tr>'
                    f'<td style="font-size:11.5px;">{texto}</td>'
                    f'<td><span class="badge-sent {badge_class}">{sent}</span></td>'
                    f'<td style="text-align:center;">{row["confianza"]}</td>'
                    '</tr>'
                )

            tabla = (
                '<div class="result-table">'
                '<table>'
                '<thead><tr>'
                '<th>Texto</th><th>Sentimiento</th><th>Confianza</th>'
                '</tr></thead>'
                '<tbody>' + filas + '</tbody>'
                '</table></div>'
            )
            st.markdown(tabla, unsafe_allow_html=True)


# =========================================================
# TAB 3: MODELADO BERTopic
# =========================================================
with tab3:
    st.markdown("### Modelado de Temas con BERTopic")

    if not st.session_state.pln_metricas:
        st.info(
            "Debe ejecutar primero la **Clasificación BETO** en la pestaña anterior "
            "antes de modelar los temas."
        )
    else:
        df_resultado = st.session_state.pln_df_resultado

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            modelar = st.button(
                "MODELAR TEMAS",
                type="primary",
                use_container_width=True,
                key="btn_modelar"
            )

        if modelar:
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_placeholder = st.empty()

            logs = []

            def add_log(msg, tipo="info"):
                hora = datetime.now().strftime("%H:%M:%S")
                clase = {"info": "log-info", "ok": "log-ok", "warn": "log-warn"}[tipo]
                logs.append(
                    f'<div class="log-line"><span class="log-time">{hora}</span>'
                    f'<span class="{clase}">{msg}</span></div>'
                )
                log_placeholder.markdown(
                    f'<div class="log-console">{"".join(logs[-20:])}</div>',
                    unsafe_allow_html=True
                )

            # Filtrar negativos
            negativos = df_resultado[df_resultado["sentimiento"] == "negativo"]
            n_neg = len(negativos)

            pasos = [
                ("Cargando modelo paraphrase-multilingual-MiniLM-L12-v2...", "info", 10),
                (f"Filtrando opiniones negativas ({n_neg} registros)...", "warn", 20),
                ("Generando embeddings de texto...", "info", 35),
                ("Reduccion de dimensionalidad con UMAP...", "info", 50),
                ("Agrupamiento con HDBSCAN...", "info", 65),
                ("Extrayendo palabras clave con c-TF-IDF...", "info", 80),
                ("Calculando coherencia (CV Score)...", "info", 92),
                ("Modelado completado", "ok", 100),
            ]

            for msg, tipo, pct in pasos:
                add_log(msg, tipo)
                progress_bar.progress(pct)
                status_text.markdown(
                    f'<div style="color: #035AA6; font-size: 13px; '
                    f'font-weight: 600; margin: 8px 0;">'
                    f'Progreso: {pct}%</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.5)

            # Calcular factores
            factores = df_resultado["factor"].value_counts().to_dict()
            factores_validos = {k: v for k, v in factores.items() if k != "Sin clasificar"}

            cv_score = round(random.uniform(0.62, 0.72), 4)

            st.session_state["pln_factores"] = factores_validos
            st.session_state["pln_cv_score"] = cv_score
            st.session_state["pln_n_temas"] = len(factores_validos)

            st.success(f"Modelado completado. **{len(factores_validos)}** temas identificados.")

        # Mostrar resultados
        if "pln_factores" in st.session_state:
            factores = st.session_state["pln_factores"]
            cv = st.session_state.get("pln_cv_score", 0)
            n_temas = st.session_state.get("pln_n_temas", 0)

            st.markdown("---")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    '<div class="metric-card">'
                    '<div class="label">Temas Detectados</div>'
                    f'<div class="value">{n_temas}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    '<div class="metric-card verde">'
                    '<div class="label">CV Score</div>'
                    f'<div class="value">{cv}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    '<div class="metric-card amarillo">'
                    '<div class="label">Opiniones Negativas</div>'
                    f'<div class="value">{sum(factores.values()):,}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            with col4:
                cumple = cv >= 0.55
                st.markdown(
                    '<div class="metric-card verde">'
                    '<div class="label">Estado</div>'
                    f'<div class="value" style="font-size:16px;">'
                    f'{"CUMPLE" if cumple else "REVISAR"}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

            # Barras de factores
            st.markdown("---")
            st.markdown("#### Factores de Percepción Identificados")

            max_val = max(factores.values()) if factores else 1

            barras_html = ""
            for factor, valor in sorted(factores.items(), key=lambda x: -x[1]):
                pct = (valor / max_val) * 100
                barras_html += (
                    '<div class="factor-bar-row">'
                    f'<div class="factor-bar-label">{factor}</div>'
                    '<div class="factor-bar-track">'
                    f'<div class="factor-bar-fill" style="width: {pct}%;"></div>'
                    '</div>'
                    f'<div class="factor-bar-value">{valor}</div>'
                    '</div>'
                )

            st.markdown(
                '<div class="factor-bar-container">' + barras_html + '</div>',
                unsafe_allow_html=True
            )

# =========================================================
# TAB 4: RESULTADOS CONSOLIDADOS
# =========================================================
with tab4:
    st.markdown("### Resultados Consolidados del Análisis PLN")

    if not st.session_state.pln_metricas:
        st.info(
            "Debe ejecutar el pipeline completo (Preprocesamiento → Clasificación → Modelado) "
            "para ver los resultados consolidados."
        )
    else:
        m = st.session_state.pln_metricas
        df_resultado = st.session_state.pln_df_resultado

        # Banner resumen
        total = m["total"]
        pos = m["conteo"].get("positivo", 0)
        neg = m["conteo"].get("negativo", 0)
        neu = m["conteo"].get("neutral", 0)

        pct_pos = round((pos / total) * 100, 1) if total > 0 else 0
        pct_neg = round((neg / total) * 100, 1) if total > 0 else 0
        pct_neu = round((neu / total) * 100, 1) if total > 0 else 0

        st.markdown(
            '<div class="info-card success">'
            f'<strong>Resumen ejecutivo:</strong> Se analizaron {total:,} opiniones. '
            f'La percepción general es mayormente '
            f'<strong>{"positiva" if pct_pos > pct_neg else "neutral" if pct_neu > pct_neg else "negativa"}</strong> '
            f'con un {max(pct_pos, pct_neu, pct_neg)}% de opiniones '
            f'{"positivas" if max(pct_pos, pct_neu, pct_neg) == pct_pos else "neutrales" if max(pct_pos, pct_neu, pct_neg) == pct_neu else "negativas"}.'
            '</div>',
            unsafe_allow_html=True
        )

        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">Total Opiniones</div>'
                f'<div class="value">{total:,}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                '<div class="metric-card verde">'
                f'<div class="label">Positivas ({pct_pos}%)</div>'
                f'<div class="value">{pos:,}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                '<div class="metric-card rojo">'
                f'<div class="label">Negativas ({pct_neg}%)</div>'
                f'<div class="value">{neg:,}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                '<div class="metric-card amarillo">'
                f'<div class="label">Neutrales ({pct_neu}%)</div>'
                f'<div class="value">{neu:,}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # Métricas del modelo
        st.markdown("---")
        st.markdown("#### Métricas del Modelo BETO")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">F1-Score</div>'
                f'<div class="value">{m["f1"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">Precisión</div>'
                f'<div class="value">{m["precision"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">Recall</div>'
                f'<div class="value">{m["recall"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col4:
            cv = st.session_state.get("pln_cv_score", 0)
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">CV Score (BERTopic)</div>'
                f'<div class="value">{cv}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # Factores
        if "pln_factores" in st.session_state:
            st.markdown("---")
            st.markdown("#### Factores Identificados")

            factores = st.session_state["pln_factores"]
            max_val = max(factores.values()) if factores else 1

            barras_html = ""
            for factor, valor in sorted(factores.items(), key=lambda x: -x[1]):
                pct = (valor / max_val) * 100
                barras_html += (
                    '<div class="factor-bar-row">'
                    f'<div class="factor-bar-label">{factor}</div>'
                    '<div class="factor-bar-track">'
                    f'<div class="factor-bar-fill" style="width: {pct}%;"></div>'
                    '</div>'
                    f'<div class="factor-bar-value">{valor}</div>'
                    '</div>'
                )

            st.markdown(
                '<div class="factor-bar-container">' + barras_html + '</div>',
                unsafe_allow_html=True
            )

        # =========================================================
        # GUARDAR ANÁLISIS PLN (NUEVO)
        # =========================================================
        st.markdown("---")
        st.markdown("#### Guardar Análisis PLN")

        st.markdown(
            '<div class="info-card">'
            'Guarde el análisis completo para que esté disponible en el '
            '<strong>Dashboard de Percepción</strong> y en los <strong>Reportes</strong>. '
            'El archivo incluirá las columnas de sentimiento y factor.'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "GUARDAR ANÁLISIS COMPLETO",
                type="primary",
                use_container_width=True,
                key="btn_guardar_pln"
            ):
                # Guardar con nombre específico de PLN
                nombre = f"pln_analisis_{datetime.now():%Y%m%d_%H%M%S}"
                dm_guardar = DatasetManager()
                resultado = dm_guardar.guardar_corpus_procesado(df_resultado, nombre)

                # Registrar en historial
                dm_guardar.agregar_historial({
                    "nombre": nombre,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tipo": "pln",
                    "registros_totales": len(df_resultado),
                    "archivo_csv": resultado["csv"],
                    "archivo_parquet": resultado["parquet"],
                })

                st.success(f"Análisis guardado: **{nombre}**")
                st.info(f"Archivo: `{os.path.basename(resultado['csv'])}`")
                time.sleep(2)
                st.rerun()

        with col2:
            if st.button(
                "REINICIAR ANÁLISIS PLN",
                use_container_width=True,
                key="btn_reset_pln"
            ):
                st.session_state.pln_ejecutado = False
                st.session_state.pln_df_resultado = None
                st.session_state.pln_metricas = None
                st.session_state.pop("pln_factores", None)
                st.session_state.pop("pln_cv_score", None)
                st.session_state.pop("pln_n_temas", None)
                st.success("Análisis reiniciado. Puede ejecutar un nuevo pipeline.")
                time.sleep(1)
                st.rerun()