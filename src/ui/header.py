# src/ui/header.py
"""
Header compartido para todos los módulos del sistema.
Barra superior azul sticky con logo y usuario.
"""

import streamlit as st


def render_header(user, logo_b64=None):
    """
    Renderiza el header superior azul institucional sticky.

    Args:
        user: dict con datos del usuario autenticado
        logo_b64: string con el logo en base64 (opcional)
    """
    if logo_b64 is None:
        from src.ui.sidebar import get_logo_base64
        logo_b64 = get_logo_base64()

    # ==== LOGO + TÍTULO ====
    if logo_b64:
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="max-height: 52px;" />'
        )
    else:
        logo_html = (
            '<div style="font-size: 32px; font-weight: 900; color: #FFF; '
            'letter-spacing: 2px; font-family: Arial, sans-serif;">EMI</div>'
        )

    inicial = user['nombre'][0].upper() if user.get('nombre') else "A"
    rol = user.get('rol', 'Administrador')

    st.markdown(
        '<div class="emi-top-header-sticky">'
        '<div class="emi-header-left">'
        f'{logo_html}'
        '<div class="emi-header-title-box">'
        '<div class="emi-header-title">Percepción Institucional</div>'
        '<div class="emi-header-subtitle">Sistema EMI - La Paz</div>'
        '</div>'
        '</div>'
        '<div class="emi-header-right">'
        f'<span class="emi-header-rol">{rol}</span>'
        f'<div class="emi-header-avatar">{inicial}</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )