# src/ui/sidebar.py
"""
Sidebar compartido para todos los módulos del sistema.
Renderiza el logo institucional y el menú de navegación.
"""

import streamlit as st


def get_logo_base64():
    """Lee el logo desde assets/logo_emi.png y lo retorna en base64."""
    import os
    import base64

    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "assets", "logo_emi.png"
    )
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def render_sidebar(user, logo_b64=None, current_page="dashboard"):
    """
    Renderiza el sidebar institucional unificado.

    Args:
        user: dict con datos del usuario autenticado
        logo_b64: string con el logo en base64 (opcional)
        current_page: identificador de la página actual
            - "dashboard"
            - "usuarios"
            - "fuentes"
            - "pln"
            - "reportes"
    """
    if logo_b64 is None:
        logo_b64 = get_logo_base64()

    with st.sidebar:
        # ==== LOGO INSTITUCIONAL ====
        if logo_b64:
            st.markdown(
                '<div class="sidebar-brand">'
                f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo" />'
                '<div class="brand-sub">PERCEPCION INSTITUCIONAL</div>'
                '<div class="brand-sub2">Sistema EMI - La Paz</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="sidebar-brand">'
                '<div class="brand-title">EMI</div>'
                '<div class="brand-sub">PERCEPCION INSTITUCIONAL</div>'
                '<div class="brand-sub2">Sistema EMI - La Paz</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # ==== ETIQUETA MÓDULOS ====
        st.markdown('<div class="sidebar-label">MODULOS</div>',
                    unsafe_allow_html=True)

        # ==== RESALTAR BOTÓN ACTIVO ====
        page_index = {
            "dashboard": 1,
            "usuarios": 2,
            "fuentes": 3,
            "pln": 4,
            "reportes": 5,
        }.get(current_page, 1)

        st.markdown(
            f'<style>'
            f'[data-testid="stSidebar"] .stButton:nth-of-type({page_index}) > button {{'
            f'background: #00539B !important; '
            f'font-weight: 700 !important; '
            f'box-shadow: inset 3px 0 0 #F2B705 !important;'
            f'}}'
            f'</style>',
            unsafe_allow_html=True
        )

        # ==== NAVEGACIÓN ====
        if st.button("Gestión de Usuarios",
                     key="nav_usuarios",
                     use_container_width=True):
            st.session_state.page = "usuarios"
            st.switch_page("pages/1_Gestion_Usuarios.py")

        if st.button("Gestión de Fuente y Recopilación",
                     key="nav_fuentes",
                     use_container_width=True):
            st.session_state.page = "fuentes"
            st.switch_page("pages/2_Gestion_Fuentes.py")

        if st.button("Procesamiento y Análisis PLN",
                     key="nav_pln",
                     use_container_width=True):
            st.session_state.page = "pln"
            st.switch_page("pages/3_Procesamiento_PLN.py")

        if st.button("Dashboard de Percepción",
                     key="nav_dashboard",
                     use_container_width=True):
            st.session_state.page = "dashboard"
            st.switch_page("pages/4_Dashboard.py")

        if st.button("Informes y Reportes",
                     key="nav_reportes",
                     use_container_width=True):
            st.session_state.page = "reportes"
            st.switch_page("pages/5_Reportes.py")

        # ==== CERRAR SESIÓN ====
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Cerrar Sesión",
                     key="nav_logout",
                     use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)