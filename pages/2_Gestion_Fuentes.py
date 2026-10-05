# pages/2_Gestion_Fuentes.py
import streamlit as st
import pandas as pd
import sys
import os
import json
import time
from datetime import datetime, date
from src.ui.sidebar import render_sidebar
from src.ui.styles import inyectar_css_global

# === MARCAR PÁGINA ACTIVA ===
st.session_state.page = "fuentes"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Gestión de Fuentes - EMI",
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
# RUTAS GLOBALES
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FUENTES_FILE = os.path.join(DATA_DIR, "fuentes_config.json")


# =========================================================
# UTILIDADES
# =========================================================
def get_logo_base64():
    import base64
    logo_path = os.path.join(BASE_DIR, "assets", "logo_emi.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def cargar_fuentes_desde_json():
    """Carga las fuentes desde el archivo JSON."""
    if not os.path.exists(FUENTES_FILE):
        return None
    try:
        with open(FUENTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def guardar_fuentes_a_json(fuentes):
    """Guarda las fuentes en el archivo JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FUENTES_FILE, "w", encoding="utf-8") as f:
        json.dump(fuentes, f, indent=2, ensure_ascii=False)


def registrar_evento_fuente(tipo_evento, fuente_data):
    """
    Registra un evento relacionado con fuentes en el historial.
    tipo_evento: "fuente_creada", "fuente_modificada", "fuente_eliminada"
    """
    try:
        from src.datasets.dataset_manager import DatasetManager
        dm = DatasetManager()
        dm.agregar_historial({
            "nombre": f"{tipo_evento}_{fuente_data.get('id', 'X')}_{datetime.now():%Y%m%d_%H%M%S}",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo_evento,
            "fuente_id": fuente_data.get("id", ""),
            "plataforma": fuente_data.get("plataforma", ""),
            "cuenta": fuente_data.get("cuenta", ""),
            "url": fuente_data.get("url", ""),
            "tipo_info": fuente_data.get("tipo", ""),
            "estado": fuente_data.get("estado", ""),
            "registros_totales": fuente_data.get("registros", 0),
        })
    except Exception:
        pass


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
        'RECOPILACION DE DATOS</div>'
        '<h1 style="font-size: 24px; font-weight: 700; color: #FFFFFF !important; '
        'margin: 0 0 8px 0 !important; padding: 0 !important; '
        'border: none !important; line-height: 1.2;">'
        'Gestión de Fuente y Recopilación</h1>'
        '<p style="font-size: 13px; color: #FFFFFF !important; margin: 0; line-height: 1.5;">'
        'Configure las fuentes de información y ejecute procesos de recopilación.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# INICIALIZAR FUENTES
# =========================================================
def inicializar_fuentes():
    """Carga las fuentes desde JSON o las inicializa por defecto."""
    if "fuentes_config" not in st.session_state:
        fuentes_guardadas = cargar_fuentes_desde_json()

        if fuentes_guardadas is not None and len(fuentes_guardadas) > 0:
            st.session_state.fuentes_config = fuentes_guardadas
        else:
            st.session_state.fuentes_config = [
                {"id": "F01", "plataforma": "Facebook",
                 "cuenta": "EMI UALP - página oficial",
                 "url": "https://www.facebook.com/EMIBolivia",
                 "tipo": "Publicaciones y comentarios",
                 "estado": "Conectada", "registros": 775},
                {"id": "F02", "plataforma": "Facebook",
                 "cuenta": "Confesiones EMI",
                 "url": "https://www.facebook.com/p/Confesiones-EMI",
                 "tipo": "Publicaciones y comentarios",
                 "estado": "Conectada", "registros": 312},
                {"id": "F03", "plataforma": "Facebook",
                 "cuenta": "Confesiones EMI 2.0",
                 "url": "https://www.facebook.com/p/Confesiones-EMI-2.0",
                 "tipo": "Publicaciones y comentarios",
                 "estado": "Conectada", "registros": 128},
                {"id": "G01", "plataforma": "Google Maps",
                 "cuenta": "EMI UALP - Rafael Pabón, La Paz",
                 "url": "https://www.google.com/maps/place/EMI+La+Paz",
                 "tipo": "Reseñas con calificación",
                 "estado": "Conectada", "registros": 229},
            ]
            guardar_fuentes_a_json(st.session_state.fuentes_config)


# =========================================================
# RENDERIZAR
# =========================================================
logo_b64 = get_logo_base64()

inyectar_css_global()
render_sidebar(user_actual, logo_b64, current_page="fuentes")
render_header(user_actual, logo_b64)
render_hero()

inicializar_fuentes()


# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["FUENTES CONFIGURADAS", "NUEVA FUENTE", "EJECUTAR SCRAPING"])


# =========================================================
# TAB 1: FUENTES CONFIGURADAS
# =========================================================
with tab1:
    st.markdown("### Fuentes de Información")

    fuentes = st.session_state.fuentes_config

    # ==== MÉTRICAS ====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Total Fuentes</div>'
            f'<div class="value">{len(fuentes)}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        activas = len([f for f in fuentes if f["estado"] == "Conectada"])
        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">Conectadas</div>'
            f'<div class="value">{activas}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        fb = len([f for f in fuentes if f["plataforma"] == "Facebook"])
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Facebook</div>'
            f'<div class="value">{fb}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        gm = len([f for f in fuentes if f["plataforma"] == "Google Maps"])
        st.markdown(
            '<div class="metric-card rojo">'
            '<div class="label">Google Maps</div>'
            f'<div class="value">{gm}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # ==== LISTA DE FUENTES (con cards) ====
    if not fuentes:
        st.info("No hay fuentes registradas.")
    else:
        for i, fuente in enumerate(fuentes):
            icono = "FB" if fuente["plataforma"] == "Facebook" else "GM"
            status_class = "status-activo" if fuente["estado"] == "Conectada" else "status-inactivo"
            card_class = "fuente-card" if fuente["estado"] == "Conectada" else "fuente-card inactiva"

            st.markdown(
                f'<div class="{card_class}">'
                '<div class="fuente-info">'
                f'<div class="fuente-icon">{icono}</div>'
                '<div>'
                f'<div class="fuente-name">{fuente["cuenta"]}</div>'
                f'<div class="fuente-desc">{fuente["plataforma"]} · {fuente["tipo"]}</div>'
                '</div>'
                '</div>'
                f'<span class="fuente-status {status_class}">{fuente["estado"]}</span>'
                '</div>',
                unsafe_allow_html=True
            )

    # ==== ADMINISTRAR FUENTE ====
    if fuentes:
        st.markdown("---")
        st.markdown("### Administrar Fuente")

        # Etiquetas para el selectbox
        etiquetas = [
            f"{f['id']} · {f['cuenta']} ({f['plataforma']})"
            for f in fuentes
        ]

        # Inicializar índice en session_state
        if "fuente_admin_idx" not in st.session_state:
            st.session_state.fuente_admin_idx = 0

        # Asegurar que el índice esté dentro de rango
        if st.session_state.fuente_admin_idx >= len(fuentes):
            st.session_state.fuente_admin_idx = 0

        # Selectbox con índice persistente
        seleccion = st.selectbox(
            "Seleccione una fuente",
            etiquetas,
            index=st.session_state.fuente_admin_idx,
            key="fuente_admin_select"
        )

        # Actualizar índice según la selección del usuario
        idx = etiquetas.index(seleccion)
        st.session_state.fuente_admin_idx = idx
        fuente = fuentes[idx]

        col_a, col_b, col_c = st.columns(3)

        # ==== BOTÓN: ACTIVAR / DESACTIVAR ====
        with col_a:
            nuevo_estado = "Inactiva" if fuente["estado"] == "Conectada" else "Conectada"
            label_btn = f"{'DESACTIVAR' if nuevo_estado == 'Inactiva' else 'ACTIVAR'} FUENTE"

            if st.button(label_btn, use_container_width=True, key="btn_toggle_fuente"):
                st.session_state.fuentes_config[idx]["estado"] = nuevo_estado
                guardar_fuentes_a_json(st.session_state.fuentes_config)
                registrar_evento_fuente(
                    "fuente_modificada",
                    st.session_state.fuentes_config[idx]
                )
                st.success(f"Fuente '{fuente['cuenta']}' {nuevo_estado.lower()}")
                time.sleep(1)
                st.rerun()

        # ==== BOTÓN: VER DETALLES ====
        with col_b:
            if st.button("VER DETALLES", use_container_width=True, key="btn_detalle"):
                st.session_state["fuente_detalle_idx"] = idx

        # ==== BOTÓN: ELIMINAR ====
        with col_c:
            if st.button("ELIMINAR FUENTE", use_container_width=True,
                         type="primary", key="btn_eliminar_fuente"):
                st.session_state["confirm_delete_fuente_idx"] = idx

        # ==== PANEL DE DETALLES ====
        if st.session_state.get("fuente_detalle_idx") is not None:
            idx_det = st.session_state["fuente_detalle_idx"]
            if idx_det < len(st.session_state.fuentes_config):
                f = st.session_state.fuentes_config[idx_det]
                st.markdown("---")
                st.markdown(f"#### Detalles de {f['id']}")
                st.markdown(
                    f'<div class="info-card">'
                    f'<strong>Plataforma:</strong> {f["plataforma"]}<br>'
                    f'<strong>Cuenta:</strong> {f["cuenta"]}<br>'
                    f'<strong>URL:</strong> {f["url"]}<br>'
                    f'<strong>Tipo:</strong> {f["tipo"]}<br>'
                    f'<strong>Estado:</strong> {f["estado"]}<br>'
                    f'<strong>Registros:</strong> {f["registros"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if st.button("Cerrar detalles", key="cerrar_detalle"):
                    st.session_state["fuente_detalle_idx"] = None
                    st.rerun()

        # ==== CONFIRMACIÓN DE ELIMINACIÓN ====
        if st.session_state.get("confirm_delete_fuente_idx") is not None:
            idx_del = st.session_state["confirm_delete_fuente_idx"]
            if idx_del < len(st.session_state.fuentes_config):
                f_del = st.session_state.fuentes_config[idx_del]

                st.warning(f"¿Está seguro de eliminar la fuente **{f_del['cuenta']}**?")

                col_x, col_y = st.columns(2)

                with col_x:
                    if st.button("Sí, eliminar", type="primary",
                                 use_container_width=True, key="confirm_del_si"):
                        registrar_evento_fuente("fuente_eliminada", f_del)

                        st.session_state.fuentes_config.pop(idx_del)
                        guardar_fuentes_a_json(st.session_state.fuentes_config)

                        # Resetear estados
                        st.session_state.fuente_admin_idx = 0
                        st.session_state["confirm_delete_fuente_idx"] = None
                        st.session_state["fuente_detalle_idx"] = None

                        st.success("Fuente eliminada")
                        time.sleep(1)
                        st.rerun()

                with col_y:
                    if st.button("Cancelar", use_container_width=True,
                                 key="confirm_del_no"):
                        st.session_state["confirm_delete_fuente_idx"] = None
                        st.rerun()


# =========================================================
# TAB 2: NUEVA FUENTE
# =========================================================
with tab2:
    st.markdown("### Registrar Nueva Fuente")

    with st.form("form_nueva_fuente", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            plataforma = st.selectbox("Plataforma *", ["Facebook", "Google Maps"])
            cuenta = st.text_input("Nombre de la cuenta o ubicación *",
                                    placeholder="ej: Confesiones EMI 3.0")
            url = st.text_input("URL de la fuente *", placeholder="https://...")

        with col2:
            tipo = st.selectbox("Tipo de información *", [
                "Publicaciones y comentarios",
                "Reseñas con calificación",
                "Comentarios y respuestas",
            ])
            descripcion = st.text_area("Descripción (opcional)",
                                        placeholder="Breve descripción",
                                        height=100)

        st.markdown("---")
        activa = st.checkbox("Activar fuente inmediatamente", value=True)

        submitted = st.form_submit_button("REGISTRAR FUENTE",
                                           use_container_width=True,
                                           type="primary")

        if submitted:
            errores = []
            if not cuenta or not url:
                errores.append("Los campos marcados con (*) son obligatorios")
            if not url.startswith("http"):
                errores.append("La URL debe comenzar con http:// o https://")

            if errores:
                for e in errores:
                    st.error(e)
            else:
                prefijo = "F" if plataforma == "Facebook" else "G"
                num = len([f for f in st.session_state.fuentes_config
                           if f["id"].startswith(prefijo)]) + 1
                nuevo_id = f"{prefijo}{num:02d}"

                nueva_fuente = {
                    "id": nuevo_id,
                    "plataforma": plataforma,
                    "cuenta": cuenta.strip(),
                    "url": url.strip(),
                    "tipo": tipo,
                    "estado": "Conectada" if activa else "Inactiva",
                    "registros": 0,
                }

                st.session_state.fuentes_config.append(nueva_fuente)
                guardar_fuentes_a_json(st.session_state.fuentes_config)
                registrar_evento_fuente("fuente_creada", nueva_fuente)

                st.success(f"Fuente **{nuevo_id}** registrada correctamente")
                st.balloons()


# =========================================================
# TAB 3: EJECUTAR SCRAPING
# =========================================================
with tab3:
    from src.datasets.dataset_manager import DatasetManager

    dm = DatasetManager()

    st.markdown("### Ejecutar Proceso de Recopilación")

    # ==== ESTADÍSTICAS ====
    fecha_min, fecha_max, stats = dm.estadisticas_por_fecha()

    if fecha_min is None:
        st.warning(
            "No se encontraron archivos CSV en `data/raw/`. "
            "Coloque sus datasets escrapeados en esa carpeta."
        )
        st.stop()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="label">Archivos Cargados</div>'
            f'<div class="value">{len(dm.listar_archivos_raw())}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card verde">'
            '<div class="label">Registros Totales</div>'
            f'<div class="value">{stats.get("total", 0):,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        por_fuente = stats.get("por_fuente", {})
        fb = por_fuente.get("facebook", 0)
        st.markdown(
            '<div class="metric-card amarillo">'
            '<div class="label">Facebook</div>'
            f'<div class="value">{fb:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        gm = por_fuente.get("google_maps", 0)
        st.markdown(
            '<div class="metric-card rojo">'
            '<div class="label">Google Maps</div>'
            f'<div class="value">{gm:,}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # ==== CONFIGURACIÓN ====
    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col1:
        fuente_sel = st.selectbox(
            "Fuente",
            ["todas", "facebook", "google_maps"],
            format_func=lambda x: {
                "todas": "Todas las fuentes",
                "facebook": "Facebook",
                "google_maps": "Google Maps"
            }.get(x, x),
            key="scraping_fuente"
        )

    with col2:
        rango_fechas = st.date_input(
            "Rango de fechas",
            value=(fecha_min, fecha_max),
            min_value=fecha_min,
            max_value=fecha_max,
            key="scraping_fechas"
        )

    with col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        iniciar = st.button(
            "INICIAR SCRAPING",
            type="primary",
            use_container_width=True,
            key="btn_iniciar_scraping"
        )

    if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
    else:
        fecha_inicio, fecha_fin = fecha_min, fecha_max

    # ==== EJECUCIÓN ====
    if iniciar:
        df_resultado = dm.simular_scraping(fuente_sel, fecha_inicio, fecha_fin)

        if len(df_resultado) == 0:
            st.warning("No se encontraron registros en el rango de fechas seleccionado.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            stat_placeholder = st.empty()
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
                    f'<div class="log-console">{"".join(logs[-18:])}</div>',
                    unsafe_allow_html=True
                )

            total = len(df_resultado)
            archivos = dm.listar_archivos_raw()

            pasos = [
                ("Iniciando navegador headless (Chromium)...", "info", 5),
                (f"Detectados {len(archivos)} archivos de origen...", "info", 12),
                (f"Conectando con {fuente_sel.replace('_', ' ').title()}...", "info", 20),
                ("Verificando sesión y cookies...", "info", 28),
                ("Realizando scroll infinito...", "info", 38),
                (f"Extrayendo registros desde {fecha_inicio} hasta {fecha_fin}...", "info", 52),
                ("Aplicando filtros de relevancia...", "warn", 65),
                ("Eliminando duplicados por hash SHA-256...", "warn", 76),
                ("Normalizando texto y metadatos...", "info", 86),
                ("Almacenando registros en CSV...", "ok", 94),
                (f"Scraping completado — {total} registros obtenidos", "ok", 100),
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

                extraidos = int(total * (pct / 100))
                nuevos = int(df_resultado["es_nuevo"].sum() * (pct / 100))

                stat_placeholder.markdown(
                    '<div class="progress-stats">'
                    '<div class="progress-stat">'
                    f'<div class="stat-value">{extraidos:,}</div>'
                    '<div class="stat-label">Extraídos</div>'
                    '</div>'
                    '<div class="progress-stat">'
                    f'<div class="stat-value">{nuevos:,}</div>'
                    '<div class="stat-label">Nuevos</div>'
                    '</div>'
                    '<div class="progress-stat">'
                    f'<div class="stat-value">{total - extraidos:,}</div>'
                    '<div class="stat-label">Pendientes</div>'
                    '</div>'
                    '<div class="progress-stat">'
                    f'<div class="stat-value">{i+1}/{len(pasos)}</div>'
                    '<div class="stat-label">Paso</div>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                time.sleep(0.5)

            st.success(
                f"Scraping completado. Se obtuvieron **{total}** registros "
                f"({int(df_resultado['es_nuevo'].sum())} nuevos)."
            )

            # Guardar el dataset procesado
            nombre_ds = f"scraping_{fuente_sel}_{datetime.now():%Y%m%d_%H%M%S}"
            df_procesado = dm.procesar_corpus(df_resultado)
            resultado = dm.guardar_corpus_procesado(df_procesado, nombre_ds)

            # Registrar en historial
            dm.agregar_historial({
                "nombre": nombre_ds,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fuente": fuente_sel,
                "fecha_inicio": str(fecha_inicio),
                "fecha_fin": str(fecha_fin),
                "registros_totales": total,
                "registros_nuevos": int(df_resultado["es_nuevo"].sum()),
                "archivos_origen": len(archivos),
                "archivo_csv": resultado["csv"],
                "archivo_parquet": resultado["parquet"],
                "tipo": "scraping",
            })

            # ==== VISTA PREVIA ====
            st.markdown("---")
            st.markdown("### Vista Previa")

            preview = df_resultado.head(8).copy()
            preview["texto_mostrar"] = preview["texto"].astype(str).str[:140] + "..."

            filas = ""
            for i, (_, row) in enumerate(preview.iterrows()):
                fuente_txt = row.get("fuente", "").replace("_", " ").title()
                estado_color = "#2E7D32" if row.get("es_nuevo", False) else "#666"
                estado_txt = "Nuevo" if row.get("es_nuevo", False) else "Existente"
                fecha_txt = row.get("fecha_dia", "—")

                filas += (
                    '<tr>'
                    f'<td style="color:#666;">{i+1}</td>'
                    f'<td><strong>{fuente_txt}</strong></td>'
                    f'<td>{row["texto_mostrar"]}</td>'
                    f'<td style="color:#666; font-size:12px;">{fecha_txt}</td>'
                    f'<td style="color:{estado_color}; font-weight:600; font-size:12px;">'
                    f'{estado_txt}</td>'
                    '</tr>'
                )

            tabla = (
                '<div class="result-table">'
                '<table>'
                '<thead><tr>'
                '<th>#</th><th>Fuente</th><th>Texto</th>'
                '<th>Fecha</th><th>Estado</th>'
                '</tr></thead>'
                '<tbody>' + filas + '</tbody>'
                '</table></div>'
            )
            st.markdown(tabla, unsafe_allow_html=True)

            # ==== BOTONES ====
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            col_x, col_y = st.columns(2)

            with col_x:
                csv_data = df_procesado.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    "Descargar Dataset Procesado (CSV)",
                    data=csv_data,
                    file_name=f"{nombre_ds}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col_y:
                if st.button("Ejecutar Nuevamente", use_container_width=True,
                              key="btn_rerun"):
                    st.rerun()

    # ==== HISTORIAL DE SCRAPING Y FUENTES ====
    st.markdown("---")
    st.markdown("### Historial de Recopilaciones y Fuentes")

    historial_completo = dm.listar_historial()
    historial = [
        h for h in historial_completo
        if h.get("tipo") in ("scraping", "fuente_creada", "fuente_eliminada", "fuente_modificada")
    ]

    if not historial:
        st.info("Aún no hay ejecuciones de scraping ni eventos de fuentes registrados.")
    else:
        for i, h in enumerate(historial):
            tipo = h.get("tipo", "scraping")

            if tipo == "scraping":
                titulo = f"**{h['nombre']}** · {h.get('fuente', '').replace('_', ' ').title()} · {h.get('registros_totales', 0):,} registros · {h['fecha']}"
            elif tipo == "fuente_creada":
                titulo = f"**Nueva fuente: {h.get('cuenta', '')}** · {h.get('plataforma', '')} · {h['fecha']}"
            elif tipo == "fuente_eliminada":
                titulo = f"**Fuente eliminada: {h.get('cuenta', '')}** · {h.get('plataforma', '')} · {h['fecha']}"
            else:
                titulo = f"**{h.get('nombre', '')}** · {h['fecha']}"

            with st.expander(titulo, expanded=False):
                col1, col2 = st.columns(2)

                with col1:
                    if tipo == "scraping":
                        st.markdown(f"""
**Detalles del scraping:**
- **Nombre:** `{h['nombre']}`
- **Fecha:** {h['fecha']}
- **Fuente:** {h.get('fuente', '').replace('_', ' ').title()}
- **Rango:** {h.get('fecha_inicio', '')} → {h.get('fecha_fin', '')}
- **Archivos origen:** {h.get('archivos_origen', 0)}
                        """)
                    else:
                        st.markdown(f"""
**Detalles del evento:**
- **Tipo:** {tipo.replace('_', ' ').title()}
- **Fecha:** {h['fecha']}
- **ID Fuente:** {h.get('fuente_id', '')}
- **Plataforma:** {h.get('plataforma', '')}
- **Cuenta:** {h.get('cuenta', '')}
- **URL:** {h.get('url', '')}
                        """)

                with col2:
                    if tipo == "scraping":
                        total_h = h.get("registros_totales", 0)
                        nuevos_h = h.get("registros_nuevos", 0)
                        st.markdown(f"""
**Métricas:**
- **Total registros:** {total_h:,}
- **Registros nuevos:** {nuevos_h:,}
- **Archivo:** `{os.path.basename(h.get('archivo_csv', ''))}`
                        """)
                    else:
                        st.markdown(f"""
**Información:**
- **Estado:** {h.get('estado', '')}
- **Tipo info:** {h.get('tipo_info', '')}
- **Registros:** {h.get('registros_totales', 0)}
                        """)

                # Botones de descarga (solo si es scraping)
                if tipo == "scraping":
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        csv_path = h.get("archivo_csv", "")
                        if csv_path and os.path.exists(csv_path):
                            with open(csv_path, "rb") as f:
                                st.download_button(
                                    "Descargar CSV",
                                    data=f.read(),
                                    file_name=os.path.basename(csv_path),
                                    mime="text/csv",
                                    use_container_width=True,
                                    key=f"dl_csv_hist_{i}"
                                )
                        else:
                            st.button("CSV no disponible", disabled=True,
                                      use_container_width=True, key=f"no_csv_{i}")

                    with col_b:
                        parquet_path = h.get("archivo_parquet")
                        if parquet_path and os.path.exists(parquet_path):
                            with open(parquet_path, "rb") as f:
                                st.download_button(
                                    "Descargar Parquet",
                                    data=f.read(),
                                    file_name=os.path.basename(parquet_path),
                                    mime="application/octet-stream",
                                    use_container_width=True,
                                    key=f"dl_pq_hist_{i}"
                                )
                        else:
                            st.button("Parquet no disponible", disabled=True,
                                      use_container_width=True, key=f"no_pq_{i}")

                    with col_c:
                        if st.button("Eliminar del historial",
                                      use_container_width=True,
                                      key=f"del_hist_{i}"):
                            st.session_state[f"confirm_del_hist_{i}"] = True

                else:
                    if st.button("Eliminar del historial",
                                  use_container_width=True,
                                  key=f"del_hist_{i}"):
                        st.session_state[f"confirm_del_hist_{i}"] = True

                # Confirmación de eliminación
                if st.session_state.get(f"confirm_del_hist_{i}"):
                    st.warning(f"¿Eliminar este registro del historial?")
                    cx, cy = st.columns(2)
                    with cx:
                        if st.button("Sí, eliminar", type="primary",
                                      use_container_width=True,
                                      key=f"conf_si_{i}"):
                            hist = dm.listar_historial()
                            hist.pop(i)
                            dm._save_history(hist)
                            st.session_state[f"confirm_del_hist_{i}"] = False
                            st.rerun()
                    with cy:
                        if st.button("Cancelar", use_container_width=True,
                                      key=f"conf_no_{i}"):
                            st.session_state[f"confirm_del_hist_{i}"] = False
                            st.rerun()