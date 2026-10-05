# app.py
# Sistema de Percepción Institucional - EMI UALP
# Punto de entrada: Login

import streamlit as st
import os
import base64
from src.auth.auth_manager import AuthManager
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="EMI - Sistema de Percepción Institucional",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# UTILIDADES
# =========================================================
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_emi.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# =========================================================
# INICIALIZACIÓN
# =========================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

auth = AuthManager()


# =========================================================
# PANTALLA DE LOGIN (NO MODIFICAR)
# =========================================================
def mostrar_login():
    logo_b64 = get_logo_base64()

    st.markdown("""
    <style>
        #MainMenu, header, footer,
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"], [data-testid="stHeader"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important; visibility: hidden !important;
        }
        html, body, .stApp, [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"] {
            background: linear-gradient(135deg, #035AA6 0%, #023d70 100%) !important;
            padding: 0 !important; margin: 0 !important; min-height: 100vh !important;
        }
        .main, .block-container, [data-testid="stAppViewBlockContainer"] {
            max-width: 100% !important;
        }
        [data-testid="stForm"] {
            background: #FFFFFF !important; border: none !important;
            border-radius: 12px !important; padding: 40px 36px 32px 36px !important;
            max-width: 400px; margin: 0 auto !important;
            box-shadow: 0 20px 50px rgba(0,0,0,0.25) !important;
            font-family: Arial, "Helvetica Neue", sans-serif !important;
        }
        .login-logo { max-width: 200px; width: 70%; margin: 0 auto 16px auto; display: block; }
        .login-fallback-logo {
            width: 56px; height: 56px; margin: 0 auto 14px auto;
            border: 2.5px solid #035AA6; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: #035AA6; font-weight: 700; font-size: 18px;
        }
        .login-title { font-size: 19px; font-weight: 700; color: #0B2440; text-align: center; margin: 4px 0 6px 0; }
        .login-subtitle { font-size: 12.5px; color: #6B7280; text-align: center; margin: 2px 0; }
        .login-divider { width: 100%; height: 4px; background: #F2B705; margin: 18px 0 22px 0; border-radius: 2px; }
        .login-footer {
            text-align: center; font-size: 11px; color: #9CA8B4;
            margin-top: 20px; padding-top: 14px; border-top: 1px solid #EEF2F7;
        }
        [data-testid="stForm"] label {
            font-size: 12.5px !important; font-weight: 600 !important; color: #0B2440 !important;
        }
        [data-testid="stForm"] input[type="text"],
        [data-testid="stForm"] input[type="password"] {
            border: 1.5px solid #E1E9F2 !important; border-radius: 6px !important;
            padding: 11px 14px !important; font-size: 14px !important;
            background: #F5F8FC !important; color: #0B2440 !important;
        }
        [data-testid="stForm"] input[type="text"]:focus,
        [data-testid="stForm"] input[type="password"]:focus {
            border-color: #035AA6 !important; background: #FFFFFF !important;
            box-shadow: 0 0 0 3px rgba(3,90,166,0.12) !important; outline: none !important;
        }
        [data-testid="stForm"] button[kind="primaryFormSubmit"],
        [data-testid="stForm"] button[kind="primary"] {
            background: #035AA6 !important; color: #FFFFFF !important;
            border: none !important; border-radius: 6px !important;
            padding: 13px !important; font-size: 14.5px !important;
            font-weight: 700 !important; width: 100% !important;
            margin-top: 8px !important;
        }
        [data-testid="stForm"] button[kind="primaryFormSubmit"]:hover,
        [data-testid="stForm"] button[kind="primary"]:hover {
            background: #023d70 !important;
        }
        [data-testid="stForm"] .stAlert {
            font-size: 12px !important; border-radius: 6px !important; margin-top: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        if logo_b64:
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="login-logo" />'
        else:
            logo_html = '<div class="login-fallback-logo">EMI</div>'

        with st.form("login_form", clear_on_submit=False):
            st.markdown(f"""
                {logo_html}
                <div class="login-title">Sistema de Percepción Institucional</div>
                <div class="login-subtitle">Escuela Militar de Ingeniería</div>
                <div class="login-subtitle">Unidad Académica La Paz</div>
                <div class="login-divider"></div>
            """, unsafe_allow_html=True)

            username = st.text_input("Usuario", placeholder="admin", key="login_user")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pass")
            submitted = st.form_submit_button("Iniciar Sesión", use_container_width=True, type="primary")

            if submitted:
                if not username or not password:
                    st.warning("Complete todos los campos")
                else:
                    resultado = auth.authenticate(username, password)
                    if resultado is None:
                        st.error("Usuario o contraseña incorrectos. Intente nuevamente.")
                    elif "error" in resultado:
                        st.error(resultado["error"])
                    else:
                        st.session_state.authenticated = True
                        st.session_state.user = resultado
                        st.session_state.page = "dashboard"
                        st.rerun()

            st.markdown('<div class="login-footer">Sistema de Percepción Institucional · v1.0.0</div>', unsafe_allow_html=True)


# =========================================================
# ENRUTADOR
# =========================================================
if not st.session_state.authenticated:
    mostrar_login()
else:
    # Redirigir al dashboard principal
    st.switch_page("pages/4_Dashboard.py")