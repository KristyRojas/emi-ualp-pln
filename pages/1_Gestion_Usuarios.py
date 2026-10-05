# pages/1_Gestion_Usuarios.py
import streamlit as st
import pandas as pd
import sys
import os
from src.ui.sidebar import render_sidebar
from src.ui.header import render_header   
from src.ui.styles import inyectar_css_global  

# === MARCAR PÁGINA ACTIVA EN EL SIDEBAR ===
st.session_state.page = "usuarios"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth.auth_manager import AuthManager
from config import ROLES


# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Gestión de Usuarios - EMI",
    page_icon="👥",
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

if user_actual['rol'] not in ["SuperAdmin", "Administrador"]:
    st.error("No tiene permisos para acceder a este módulo")
    st.stop()

auth = AuthManager()


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
# HERO CARD
# =========================================================
def render_hero():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d47a1 0%, #035AA6 100%);
                color: #FFFFFF; padding: 24px 28px; border-radius: 10px;
                margin: 24px 0 24px 0;
                box-shadow: 0 4px 12px rgba(13,71,161,0.25);">
        <div style="font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
                    color: rgba(255,255,255,0.8); margin-bottom: 8px; font-weight: 600;">
            ADMINISTRACION DEL SISTEMA
        </div>
        <h1 style="font-size: 24px; font-weight: 700; color: #FFFFFF !important;
                   margin: 0 0 8px 0 !important; padding: 0 !important;
                   border: none !important; line-height: 1.2;">
            Gestión de Usuarios
        </h1>
        <p style="font-size: 13px; color: rgba(0,0,0,0); margin: 0; line-height: 1.5;">
            Cree, consulte, modifique y administre los usuarios y roles del sistema.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# RENDERIZAR
# =========================================================
logo_b64 = get_logo_base64()

inyectar_css_global()
render_sidebar(user_actual, logo_b64, current_page="usuarios")
render_header(user_actual)
render_hero()


# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["LISTADO", "CREAR USUARIO", "EDITAR / ELIMINAR"])


# =========================================================
# TAB 1: LISTADO
# =========================================================
with tab1:
    usuarios = auth.listar_usuarios()

    if not usuarios:
        st.info("No hay usuarios registrados en el sistema.")
    else:
        df = pd.DataFrame(usuarios)

        # --- MÉTRICAS ---
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="label">Total Usuarios</div>'
                f'<div class="value">{len(df)}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                '<div class="metric-card verde">'
                '<div class="label">Activos</div>'
                f'<div class="value">{len(df[df["estado"] == True])}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                '<div class="metric-card rojo">'
                '<div class="label">Inactivos</div>'
                f'<div class="value">{len(df[df["estado"] == False])}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                '<div class="metric-card amarillo">'
                '<div class="label">SuperAdmins</div>'
                f'<div class="value">{len(df[df["rol"] == "SuperAdmin"])}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

        # --- FILTROS ---
        st.markdown("### Filtros de Búsqueda")
        col_f1, col_f2, col_f3 = st.columns([1, 1, 2])

        with col_f1:
            filtro_rol = st.selectbox("Rol", ["Todos"] + ROLES, key="filtro_rol_list")

        with col_f2:
            filtro_estado = st.selectbox("Estado", ["Todos", "Activos", "Inactivos"],
                                          key="filtro_estado_list")

        with col_f3:
            busqueda = st.text_input("Buscar", placeholder="Nombre o usuario...",
                                     key="busqueda_list")

        # Aplicar filtros
        df_filtrado = df.copy()
        if filtro_rol != "Todos":
            df_filtrado = df_filtrado[df_filtrado["rol"] == filtro_rol]
        if filtro_estado == "Activos":
            df_filtrado = df_filtrado[df_filtrado["estado"] == True]
        elif filtro_estado == "Inactivos":
            df_filtrado = df_filtrado[df_filtrado["estado"] == False]
        if busqueda:
            b = busqueda.lower()
            df_filtrado = df_filtrado[
                df_filtrado["username"].str.lower().str.contains(b) |
                df_filtrado["nombre"].str.lower().str.contains(b)
            ]

        st.markdown(f"**{len(df_filtrado)}** usuarios encontrados")

        # --- TABLA HTML (estilo Card institucional) ---
        filas = ""
        for _, u in df_filtrado.iterrows():
            rol_clase = {
                "SuperAdmin": "user-badge-superadmin",
                "Administrador": "user-badge-administrador",
                "Usuario": "user-badge-usuario"
            }.get(u["rol"], "user-badge-usuario")

            if u["estado"]:
                estado_html = (
                    '<span class="user-estado user-estado-activo">'
                    '<span class="user-estado-dot"></span>'
                    'Activo</span>'
                )
            else:
                estado_html = (
                    '<span class="user-estado user-estado-inactivo">'
                    '<span class="user-estado-dot"></span>'
                    'Inactivo</span>'
                )

            ultimo_raw = u["ultimo_acceso"]
            if ultimo_raw == "Nunca" or ultimo_raw is None:
                ultimo = "None"
            else:
                ultimo_str = str(ultimo_raw)
                if "T" in ultimo_str:
                    ultimo = ultimo_str.split("T")[0]
                elif " " in ultimo_str:
                    ultimo = ultimo_str.split(" ")[0]
                else:
                    ultimo = ultimo_str

            filas += (
                '<tr>'
                f'<td class="col-usuario">{u["username"]}</td>'
                f'<td class="col-nombre">{u["nombre"]}</td>'
                f'<td class="col-cargo">{u["cargo"] or "—"}</td>'
                f'<td class="col-rol">'
                f'<span class="user-badge {rol_clase}">{u["rol"]}</span>'
                f'</td>'
                f'<td class="col-estado">{estado_html}</td>'
                f'<td class="col-ultimo">{ultimo}</td>'
                '</tr>'
            )

        tabla_html = (
            '<div class="user-table-wrapper">'
            '<table class="user-table">'
            '<thead>'
            '<tr>'
            '<th>Usuario</th>'
            '<th>Nombre</th>'
            '<th>Cargo</th>'
            '<th>Rol</th>'
            '<th>Estado</th>'
            '<th>Último Acceso</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            + filas +
            '</tbody>'
            '</table>'
            '</div>'
        )

        st.markdown(tabla_html, unsafe_allow_html=True)

# =========================================================
# TAB 2: CREAR USUARIO
# =========================================================
with tab2:
    st.markdown("### Registrar Nuevo Usuario")
    st.markdown("""
    <div class="info-card">
        Complete los campos obligatorios marcados con (*). La contraseña debe tener 
        al menos 6 caracteres y el nombre de usuario no puede contener espacios.
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_crear_usuario", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Datos de acceso**")
            username = st.text_input("Nombre de Usuario *",
                                     placeholder="ej: jperez",
                                     help="Sin espacios, sin mayúsculas")
            password = st.text_input("Contraseña *", type="password",
                                     placeholder="Mínimo 6 caracteres")
            password_confirm = st.text_input("Confirmar Contraseña *",
                                             type="password",
                                             placeholder="Repita la contraseña")

        with col2:
            st.markdown("**Datos personales**")
            nombre = st.text_input("Nombre Completo *",
                                   placeholder="ej: Juan Pérez Mamani")
            cargo = st.text_input("Cargo",
                                  placeholder="ej: Analista de Sistemas")
            rol = st.selectbox("Rol *", ROLES)

        st.markdown("---")
        estado = st.checkbox("Usuario habilitado para iniciar sesión", value=True)

        submitted = st.form_submit_button("REGISTRAR USUARIO",
                                           use_container_width=True,
                                           type="primary")

        if submitted:
            errores = []
            if not username or not nombre or not password:
                errores.append("Los campos marcados con (*) son obligatorios")
            if password != password_confirm:
                errores.append("Las contraseñas no coinciden")
            if len(password) < 6:
                errores.append("La contraseña debe tener al menos 6 caracteres")
            if " " in username:
                errores.append("El nombre de usuario no puede contener espacios")

            if errores:
                for e in errores:
                    st.error(e)
            else:
                exito, mensaje = auth.crear_usuario(
                    username=username.strip(),
                    password=password,
                    nombre=nombre.strip(),
                    cargo=cargo.strip(),
                    rol=rol,
                    estado=estado
                )
                if exito:
                    st.success(mensaje)
                    st.balloons()
                else:
                    st.error(mensaje)


# =========================================================
# TAB 3: EDITAR / ELIMINAR
# =========================================================
with tab3:
    usuarios = auth.listar_usuarios()

    if not usuarios:
        st.info("No hay usuarios para editar.")
    else:
        st.markdown("### Seleccionar Usuario")
        opciones = {f"{u['username']} — {u['nombre']} ({u['rol']})": u['username']
                    for u in usuarios}
        seleccion = st.selectbox("Usuario a gestionar", list(opciones.keys()),
                                  key="select_user_edit")
        username_sel = opciones[seleccion]
        user_data = auth.users[username_sel]

        # --- INFO DEL USUARIO ---
        st.markdown("---")
        col_info1, col_info2, col_info3 = st.columns(3)

        with col_info1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Usuario</div>
                <div class="value" style="font-size:16px;">{username_sel}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_info2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Rol Actual</div>
                <div class="value" style="font-size:16px;">{user_data['rol']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_info3:
            estado_actual = "Activo" if user_data.get('estado', True) else "Inactivo"
            color = "verde" if user_data.get('estado', True) else "rojo"
            st.markdown(f"""
            <div class="metric-card {color}">
                <div class="label">Estado</div>
                <div class="value" style="font-size:16px;">{estado_actual}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # --- FORMULARIO DE EDICIÓN ---
        st.markdown("### Modificar Datos")

        with st.form("form_modificar_usuario"):
            col1, col2 = st.columns(2)

            with col1:
                nuevo_nombre = st.text_input("Nombre Completo",
                                              value=user_data["nombre"])
                nuevo_cargo = st.text_input("Cargo",
                                             value=user_data.get("cargo", ""))

            with col2:
                nuevo_rol = st.selectbox("Rol", ROLES,
                                          index=ROLES.index(user_data["rol"]))
                nuevo_estado = st.checkbox("Usuario habilitado",
                                            value=user_data.get("estado", True))

            st.markdown("---")
            st.markdown("**Cambiar contraseña** (opcional, dejar vacío para no cambiar)")
            nueva_password = st.text_input("Nueva Contraseña", type="password",
                                            placeholder="••••••••",
                                            key="edit_pass")

            submitted_edit = st.form_submit_button("GUARDAR CAMBIOS",
                                                    use_container_width=True,
                                                    type="primary")

            if submitted_edit:
                kwargs = {
                    "nombre": nuevo_nombre.strip(),
                    "cargo": nuevo_cargo.strip(),
                    "rol": nuevo_rol,
                    "estado": nuevo_estado
                }
                if nueva_password:
                    if len(nueva_password) < 6:
                        st.error("La contraseña debe tener al menos 6 caracteres")
                    else:
                        kwargs["password"] = nueva_password

                if "password" not in kwargs or len(nueva_password) >= 6:
                    exito, mensaje = auth.modificar_usuario(username_sel, **kwargs)
                    if exito:
                        st.success(mensaje)
                        st.rerun()
                    else:
                        st.error(mensaje)

        # --- ACCIONES PELIGROSAS ---
        st.markdown("---")
        st.markdown("### Acciones sobre el Usuario")

        st.markdown("""
        <div class="info-card warning">
            Las siguientes acciones afectan directamente al usuario seleccionado. 
            Proceda con precaución.
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            if user_data.get('estado', True):
                label_btn = "DESHABILITAR USUARIO"
            else:
                label_btn = "HABILITAR USUARIO"

            if st.button(label_btn, use_container_width=True, key="btn_estado"):
                nuevo_estado_toggle = not user_data.get("estado", True)
                exito, msg = auth.cambiar_estado(username_sel, nuevo_estado_toggle)
                if exito:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with col_b:
            if st.button("ELIMINAR USUARIO", use_container_width=True,
                         type="primary", key="btn_eliminar"):
                st.session_state["confirm_delete"] = username_sel

        # --- CONFIRMACIÓN ---
        if st.session_state.get("confirm_delete") == username_sel:
            st.warning(f"¿Está seguro de eliminar al usuario **{username_sel}**? Esta acción no se puede deshacer.")

            col_x, col_y = st.columns(2)
            with col_x:
                if st.button("Sí, eliminar", use_container_width=True,
                             type="primary", key="confirm_si"):
                    exito, msg = auth.eliminar_usuario(username_sel)
                    st.session_state["confirm_delete"] = None
                    if exito:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with col_y:
                if st.button("Cancelar", use_container_width=True, key="confirm_no"):
                    st.session_state["confirm_delete"] = None
                    st.rerun()