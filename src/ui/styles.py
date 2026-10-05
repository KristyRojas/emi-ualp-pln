# src/ui/styles.py
"""
Estilos CSS compartidos para todos los módulos del sistema.
"""

import streamlit as st


def inyectar_css_global():
    """Inyecta el CSS base compartido por todos los módulos."""
    st.markdown("""
    <style>
        /* ============================================================
           OCULTAR ELEMENTOS DE STREAMLIT
           ============================================================ */
        #MainMenu, header, footer,
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stHeader"], [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"], [data-testid="stSidebarNavSeparator"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
        }

        /* ============================================================
           FONDO GLOBAL
           ============================================================ */
        .stApp, [data-testid="stAppViewContainer"] {
            background: #F5F7FA !important;
        }

        .block-container {
            padding-top: 0 !important;
            padding-bottom: 1rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 1400px !important;
        }

        /* ============================================================
           TEXTO OSCURO EN CONTENIDO PRINCIPAL
           ============================================================ */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span:not(.keep-white),
        [data-testid="stMarkdownContainer"] li,
        .stTextInput label, .stSelectbox label, .stTextArea label,
        .stNumberInput label, .stDateInput label,
        .stCheckbox label, .stCheckbox label p,
        [data-testid="stWidgetLabel"] p {
            color: #0B2440 !important;
        }

        /* ============================================================
           HEADER, SIDEBAR, HERO → BLANCO
           ============================================================ */
        .emi-top-header, .emi-top-header * {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        .emi-hero, .emi-hero * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* ============================================================
           SIDEBAR
           ============================================================ */
        [data-testid="stSidebar"] {
            background: #003B73 !important;
            border-right: none !important;
            min-width: 250px !important;
            max-width: 260px !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 0 !important;
            background: #003B73 !important;
        }
        [data-testid="stSidebar"] > div > div:first-child {
            padding: 0 !important;
        }
        [data-testid="stSidebar"] > div {
            background: #003B73 !important;
        }

        .sidebar-brand {
            padding: 22px 20px 18px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        .sidebar-brand .brand-logo {
            max-width: 130px;
            display: block;
            margin: 0 auto 10px auto;
        }
        .sidebar-brand .brand-title {
            font-size: 18px;
            font-weight: 900;
            color: #FFFFFF !important;
            letter-spacing: 2px;
            font-family: Arial, sans-serif;
            line-height: 1;
        }
        .sidebar-brand .brand-sub {
            font-size: 10px;
            color: rgba(255,255,255,0.75) !important;
            margin-top: 6px;
            letter-spacing: 0.5px;
        }
        .sidebar-brand .brand-sub2 {
            font-size: 9px;
            color: rgba(255,255,255,0.55) !important;
            margin-top: 2px;
        }

        .sidebar-label {
            font-size: 11px;
            font-weight: 700;
            color: rgba(255,255,255,0.55) !important;
            text-transform: uppercase;
            letter-spacing: 1.8px;
            padding: 22px 22px 10px 22px;
        }

        /* === BOTONES DEL SIDEBAR === */
        [data-testid="stSidebar"] .stButton {
            margin: 0 12px 4px 12px !important;
            padding: 0 !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 16px !important;
            font-size: 12px !important;
            font-weight: 400 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            width: 100% !important;
            margin: 0 !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
            line-height: 1.25 !important;
        }
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] .stButton > button div {
            color: #FFFFFF !important;
            font-size: 12px !important;
            line-height: 1.25 !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.08) !important;
        }
        [data-testid="stSidebar"] .stButton > button:focus {
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stSidebar"] .logout-btn .stButton > button {
            border-top: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 0 !important;
            margin-top: 10px !important;
            padding-top: 14px !important;
        }
        [data-testid="stSidebar"] .logout-btn .stButton > button p {
            color: rgba(255,255,255,0.7) !important;
        }
        [data-testid="stSidebar"] .logout-btn .stButton > button:hover {
            background: rgba(255, 107, 107, 0.1) !important;
        }
        [data-testid="stSidebar"] .logout-btn .stButton > button:hover p {
            color: #FF6B6B !important;
        }

        /* ============================================================
           INPUTS
           ============================================================ */
        .stTextInput input, .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input, .stDateInput input {
            border: 1.5px solid #E1E9F2 !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
            font-size: 13.5px !important;
            background: #F5F8FC !important;
            color: #0B2440 !important;
            font-weight: 500 !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #035AA6 !important;
            background: #FFFFFF !important;
            box-shadow: 0 0 0 3px rgba(3,90,166,0.12) !important;
        }
        [data-baseweb="popover"] div, [data-baseweb="popover"] li,
        [role="option"] {
            color: #0B2440 !important;
            background: #FFFFFF !important;
        }
        [role="option"]:hover {
            background: #E8F1F9 !important;
        }

        /* ============================================================
           BOTONES GENERALES
           ============================================================ */
        .stButton > button {
            background: #FFFFFF !important;
            border: 1.5px solid #E1E9F2 !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: #0B2440 !important;
        }
        .stButton > button:hover {
            border-color: #035AA6 !important;
            background: #F5F8FC !important;
        }
        .stButton > button:hover p {
            color: #035AA6 !important;
        }

        .stButton > button[kind="primary"],
        [data-testid="stBaseButton-primary"] {
            background: #035AA6 !important;
            border: none !important;
        }
        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span,
        .stButton > button[kind="primary"] div,
        [data-testid="stBaseButton-primary"] p {
            color: #FFFFFF !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: #023d70 !important;
        }

        /* ============================================================
           MÉTRICAS
           ============================================================ */
        .metric-card {
            background: #FFFFFF;
            border-radius: 8px;
            padding: 18px 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            border-top: 5px solid #035AA6;
        }
        .metric-card.verde {
            border-top-color: #2E7D32;
        }
        .metric-card.rojo {
            border-top-color: #C62828;
        }
        .metric-card.amarillo {
            border-top-color: #F2B705;
        }
        .metric-card .label {
            font-size: 11.5px;
            color: #666 !important;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .metric-card .value {
            font-size: 30px;
            font-weight: 700;
            line-height: 1;
            color: #1A1A1A !important;
        }
        .metric-card.verde .value {
            color: #2E7D32 !important;
        }
        .metric-card.rojo .value {
            color: #C62828 !important;
        }
        .metric-card.amarillo .value {
            color: #B8860B !important;
        }

        /* ============================================================
           INFO CARDS
           ============================================================ */
        .info-card {
            background: #E8F1F9;
            border-left: 4px solid #035AA6;
            border-radius: 8px;
            padding: 16px 20px;
            font-size: 12.5px;
            color: #024080 !important;
            -webkit-text-fill-color: #024080 !important;
            margin-bottom: 16px;
            line-height: 1.6;
        }
        .info-card strong {
            color: #024080 !important;
            -webkit-text-fill-color: #024080 !important;
        }

        /* ============================================================
           TABS
           ============================================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            border-bottom: 2px solid #E0E4EA;
            background: transparent;
            margin-bottom: 24px;
            margin-top: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 12px 24px;
            font-size: 13px;
            font-weight: 600;
            color: #666 !important;
            height: auto;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #035AA6 !important;
        }
        .stTabs [aria-selected="true"] {
            background: transparent;
            color: #035AA6 !important;
            border-bottom: 3px solid #035AA6;
            font-weight: 700;
        }

        /* ============================================================
           TABLAS DE RESULTADOS (result-table)
           ============================================================ */
        .result-table {
            background: #FFFFFF;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            margin-top: 16px;
        }
        .result-table table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
        }
        .result-table thead th {
            background: #003B73;
            text-align: left;
            padding: 12px 14px;
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .result-table thead th * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .result-table tbody td {
            padding: 11px 14px;
            border-bottom: 1px solid #EEF1F5;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            vertical-align: middle;
        }
        .result-table tbody td *,
        .result-table tbody td strong,
        .result-table tbody td span:not([class*="badge"]) {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .result-table tbody tr:hover {
            background: #F8FAFC;
        }
        .result-table tbody tr:last-child td {
            border-bottom: none;
        }

        /* Colores específicos dentro de result-table */
        .result-table td[style*="color:#2E7D32"],
        .result-table td[style*="color:#2E7D32"] * {
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }
        .result-table td[style*="color:#C62828"],
        .result-table td[style*="color:#C62828"] * {
            color: #C62828 !important;
            -webkit-text-fill-color: #C62828 !important;
        }
        .result-table td[style*="color:#666"],
        .result-table td[style*="color:#666"] * {
            color: #666666 !important;
            -webkit-text-fill-color: #666666 !important;
        }

        /* ============================================================
           TABLAS DENTRO DE CHART-CARD (Categorías del Dashboard)
           ============================================================ */
        .chart-card table,
        .chart-card table thead,
        .chart-card table tbody,
        .chart-card table tr,
        .chart-card table th,
        .chart-card table td,
        .chart-card table strong,
        .chart-card table span,
        .chart-card table div,
        .chart-card table * {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .chart-card table th {
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
        }

        /* ============================================================
           BADGES DE SENTIMIENTO
           ============================================================ */
        .badge-sent {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-positivo {
            background: #EAF5EA;
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }
        .badge-negativo {
            background: #FCEAEA;
            color: #C62828 !important;
            -webkit-text-fill-color: #C62828 !important;
        }
        .badge-neutral {
            background: #FFF4E0;
            color: #B8860B !important;
            -webkit-text-fill-color: #B8860B !important;
        }

        /* ============================================================
           BADGES DE FUENTE
           ============================================================ */
        .badge-fuente {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 10.5px;
            font-weight: 600;
        }
        .badge-facebook {
            background: #E8F1F9;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
        }
        .badge-google {
            background: #EAF5EA;
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }

        /* ============================================================
           TABLA DE GESTIÓN DE USUARIOS — Estilo Card
           ============================================================ */
        .user-table-wrapper {
            background: #FFFFFF;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            border: 1px solid #E2E8F0;
            overflow: hidden;
            margin-top: 16px;
        }
        .user-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            font-family: 'Segoe UI', Arial, sans-serif;
            table-layout: auto;
        }

        /* === ENCABEZADO === */
        .user-table thead th {
            background: #003366;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-align: left;
            padding: 14px 20px;
            font-size: 11.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-right: 1px solid rgba(255, 255, 255, 0.15);
            white-space: nowrap;
        }
        .user-table thead th:first-child {
            border-top-left-radius: 8px;
        }
        .user-table thead th:last-child {
            border-top-right-radius: 8px;
            border-right: none;
        }
        .user-table thead th * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* === CUERPO === */
        .user-table tbody td {
            padding: 14px 20px;
            border-bottom: 1px solid #F1F5F9;
            color: #1E293B !important;
            -webkit-text-fill-color: #1E293B !important;
            vertical-align: middle;
            font-size: 13px;
        }
        .user-table tbody tr:last-child td {
            border-bottom: none;
        }
        .user-table tbody tr:hover {
            background: #F8FAFC;
        }
        .user-table tbody td * {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }

        /* === COLUMNAS ESPECÍFICAS === */
        .user-table .col-usuario {
            font-weight: 700;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            width: 130px;
        }
        .user-table .col-nombre {
            color: #334155 !important;
            -webkit-text-fill-color: #334155 !important;
            min-width: 180px;
        }
        .user-table .col-cargo {
            color: #475569 !important;
            -webkit-text-fill-color: #475569 !important;
            min-width: 160px;
        }
        .user-table .col-rol {
            width: 160px;
        }
        .user-table .col-estado {
            width: 120px;
        }
        .user-table .col-ultimo {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-size: 12.5px;
            width: 130px;
        }

        /* === BADGES DE ROL (Pills) === */
        .user-badge {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            line-height: 1.3;
            text-align: center;
            white-space: nowrap;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .user-badge-superadmin {
            background: #DBEAFE;
            color: #0369A1 !important;
            -webkit-text-fill-color: #0369A1 !important;
        }
        .user-badge-administrador {
            background: #FEF3C7;
            color: #B45309 !important;
            -webkit-text-fill-color: #B45309 !important;
        }
        .user-badge-usuario {
            background: #E0E7FF;
            color: #3730A3 !important;
            -webkit-text-fill-color: #3730A3 !important;
        }

        /* === ESTADO CON DOT === */
        .user-estado {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 500;
        }
        .user-estado-dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .user-estado-activo {
            color: #15803D !important;
            -webkit-text-fill-color: #15803D !important;
        }
        .user-estado-activo .user-estado-dot {
            background: #16A34A;
        }
        .user-estado-inactivo {
            color: #991B1B !important;
            -webkit-text-fill-color: #991B1B !important;
        }
        .user-estado-inactivo .user-estado-dot {
            background: #DC2626;
        }

        /* ============================================================
           VISTA PREVIA DEL REPORTE (doc-preview)
           ============================================================ */
        .doc-preview,
        .doc-preview * {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 40px 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            max-width: 850px;
            margin: 0 auto;
        }
        .doc-preview .doc-title {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-subtitle {
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
        }
        .doc-preview .doc-meta {
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
        }
        .doc-preview .doc-section h3 {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-section p,
        .doc-preview .doc-section strong {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-metric .num {
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
        }
        .doc-preview .doc-metric .lbl {
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
        }
        .doc-preview .doc-table th,
        .doc-preview .doc-table td {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-footer {
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
        }
        
                /* ============================================================
           LOG DE CONSOLA (Procesamiento PLN y Scraping)
           ============================================================ */
        .log-console {
            background: #0B2440 !important;
            padding: 18px 22px;
            border-radius: 8px;
            max-height: 320px;
            overflow-y: auto;
            margin-top: 16px;
            line-height: 1.8;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 12.5px;
            border: 1px solid #1E3A5F;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
        }
        .log-console .log-line {
            margin: 3px 0;
            color: #A8D5FF !important;
            -webkit-text-fill-color: #A8D5FF !important;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 12.5px;
        }
        .log-console .log-line span {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }

        /* === COLORES POR TIPO DE MENSAJE === */
        .log-console .log-info {
            color: #A8D5FF !important;
            -webkit-text-fill-color: #A8D5FF !important;
        }
        .log-console .log-warn {
            color: #FCD34D !important;
            -webkit-text-fill-color: #FCD34D !important;
        }
        .log-console .log-error {
            color: #FCA5A5 !important;
            -webkit-text-fill-color: #FCA5A5 !important;
        }
        .log-console .log-ok {
            color: #6EE7B7 !important;
            -webkit-text-fill-color: #6EE7B7 !important;
            font-weight: 600;
        }

        /* === TIMESTAMP === */
        .log-console .log-time {
            color: #6B8DB5 !important;
            -webkit-text-fill-color: #6B8DB5 !important;
            margin-right: 12px;
            font-weight: 500;
        }

        /* === MENSAJE FINAL DE COMPLETADO (destacado) === */
        .log-console .log-final {
            color: #6EE7B7 !important;
            -webkit-text-fill-color: #6EE7B7 !important;
            font-weight: 700;
            background: rgba(110, 231, 183, 0.1);
            padding: 6px 10px;
            border-radius: 4px;
            border-left: 3px solid #6EE7B7;
            margin-top: 6px;
            display: block;
        }

        /* === ÍCONO DE CHECK PARA OK === */
        .log-console .log-ok::before {
            content: "✓  ";
            color: #6EE7B7 !important;
            -webkit-text-fill-color: #6EE7B7 !important;
            font-weight: 700;
        }
        .log-console .log-warn::before {
            content: "⚠  ";
            color: #FCD34D !important;
            -webkit-text-fill-color: #FCD34D !important;
            font-weight: 700;
        }
        .log-console .log-error::before {
            content: "✗  ";
            color: #FCA5A5 !important;
            -webkit-text-fill-color: #FCA5A5 !important;
            font-weight: 700;
        }

        /* === BARRA DE PROGRESO === */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 50%, #6EE7B7 100%) !important;
        }

        /* === ESTADÍSTICAS DEL PROCESO === */
        .progress-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 16px 0;
        }
        .progress-stat {
            text-align: center;
            padding: 14px 10px;
            background: #FFFFFF;
            border: 1px solid #E0E4EA;
            border-radius: 8px;
        }
        .progress-stat .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
            line-height: 1;
        }
        .progress-stat .stat-label {
            font-size: 10.5px;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
            margin-top: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        /* === ESTADO TEXT (Barra de progreso) === */
        .progress-text {
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
            font-size: 13px;
            font-weight: 600;
            margin: 8px 0;
        }

        /* ============================================================
           FACTORES DE PERCEPCIÓN (Barras horizontales)
           ============================================================ */
        .factor-bar-container {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            margin-top: 16px;
        }
        .factor-bar-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 14px;
        }
        .factor-bar-row:last-child {
            margin-bottom: 0;
        }
        .factor-bar-label {
            font-size: 12.5px;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            font-weight: 500;
            width: 180px;
            flex-shrink: 0;
        }
        .factor-bar-track {
            flex: 1;
            background: #EEF1F5;
            border-radius: 4px;
            height: 22px;
            overflow: hidden;
        }
        .factor-bar-fill {
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);
            transition: width 0.6s ease;
        }
        .factor-bar-value {
            font-size: 12.5px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            width: 50px;
            text-align: right;
            flex-shrink: 0;
        }

        /* ============================================================
           CHART CARDS (Tarjetas de gráficos)
           ============================================================ */
        .chart-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            height: 100%;
        }
        .chart-card h3 {
            font-size: 14px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 18px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid #EEF1F5;
        }

        /* ============================================================
           VISTA PREVIA DEL REPORTE (doc-preview)
           ============================================================ */
        .doc-preview {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 40px 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            max-width: 850px;
            margin: 0 auto;
        }
        .doc-preview,
        .doc-preview * {
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #003B73;
            margin-bottom: 24px;
        }
        .doc-preview .doc-logo {
            max-width: 140px;
            display: block;
            margin: 0 auto 12px auto;
        }
        .doc-preview .doc-title {
            font-size: 16px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 4px 0;
        }
        .doc-preview .doc-subtitle {
            font-size: 13px;
            font-weight: 700;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
            margin: 0 0 4px 0;
        }
        .doc-preview .doc-meta {
            font-size: 10.5px;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
            margin-top: 8px;
        }
        .doc-preview .doc-section {
            margin-bottom: 22px;
        }
        .doc-preview .doc-section h3 {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid #E0E4EA;
        }
        .doc-preview .doc-section p {
            font-size: 12px;
            line-height: 1.7;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 8px 0;
        }
        .doc-preview .doc-metrics {
            display: flex;
            gap: 12px;
            margin: 12px 0;
        }
        .doc-preview .doc-metric {
            flex: 1;
            padding: 12px;
            border: 1.5px solid #E0E4EA;
            border-radius: 6px;
            text-align: center;
        }
        .doc-preview .doc-metric .num {
            font-size: 18px;
            font-weight: 700;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
        }
        .doc-preview .doc-metric .lbl {
            font-size: 9.5px;
            text-transform: uppercase;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        .doc-preview .doc-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            margin-top: 8px;
        }
        .doc-preview .doc-table th {
            background: #F5F7FA;
            text-align: left;
            padding: 8px;
            border-bottom: 1.5px solid #003B73;
            font-size: 10px;
            text-transform: uppercase;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-table td {
            padding: 8px;
            border-bottom: 1px solid #EEF1F5;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
        }
        .doc-preview .doc-footer {
            margin-top: 30px;
            padding-top: 12px;
            border-top: 2px solid #003B73;
            text-align: center;
            font-size: 9.5px;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
        }
        
                /* ============================================================
           CARDS DE FUENTES (Gestión de Fuente y Recopilación)
           ============================================================ */
        .fuente-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 18px 22px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            border-left: 4px solid #035AA6;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .fuente-card:hover {
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            transform: translateY(-1px);
        }
        .fuente-card.inactiva {
            border-left-color: #A0B4C8;
            opacity: 0.75;
        }

        .fuente-card .fuente-info {
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1;
        }

        .fuente-card .fuente-icon {
            width: 46px;
            height: 46px;
            border-radius: 8px;
            background: #E8F1F9;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 16px;
            flex-shrink: 0;
            letter-spacing: 0.5px;
        }

        .fuente-card .fuente-name {
            font-size: 14px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0;
            line-height: 1.3;
        }

        .fuente-card .fuente-desc {
            font-size: 12px;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
            margin: 4px 0 0 0;
            line-height: 1.4;
        }

        .fuente-card .fuente-status {
            font-size: 11.5px;
            font-weight: 700;
            padding: 5px 14px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
            flex-shrink: 0;
        }
        .fuente-card .status-activo {
            background: #EAF5EA;
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }
        .fuente-card .status-inactivo {
            background: #F5F5F5;
            color: #999 !important;
            -webkit-text-fill-color: #999 !important;
        }
        
                /* ============================================================
           COLORES DE SENTIMIENTO NETO EN TABLAS
           ============================================================ */
        .sent-neto-positivo {
            color: #15803D !important;
            -webkit-text-fill-color: #15803D !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .sent-neto-negativo {
            color: #DC2626 !important;
            -webkit-text-fill-color: #DC2626 !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .sent-neto-cero {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-weight: 600 !important;
            text-align: right;
        }

        /* Asegurar que las clases ganen sobre el CSS genérico de la tabla */
        .result-table tbody td.sent-neto-positivo,
        .result-table tbody td.sent-neto-positivo * {
            color: #15803D !important;
            -webkit-text-fill-color: #15803D !important;
        }
        .result-table tbody td.sent-neto-negativo,
        .result-table tbody td.sent-neto-negativo * {
            color: #DC2626 !important;
            -webkit-text-fill-color: #DC2626 !important;
        }
        .result-table tbody td.sent-neto-cero,
        .result-table tbody td.sent-neto-cero * {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
        }
        
                /* ============================================================
           SENTIMIENTO NETO EN TABLAS (verde / rojo / gris)
           ============================================================ */
        .result-table td.sent-neto-positivo,
        .result-table td.sent-neto-positivo * {
            color: #15803D !important;
            -webkit-text-fill-color: #15803D !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .result-table td.sent-neto-negativo,
        .result-table td.sent-neto-negativo * {
            color: #DC2626 !important;
            -webkit-text-fill-color: #DC2626 !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .result-table td.sent-neto-cero,
        .result-table td.sent-neto-cero * {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-weight: 600 !important;
            text-align: right;
        }
        
                /* ============================================================
           FACTORES DE PERCEPCIÓN — Barras horizontales
           ============================================================ */
        .factor-bar-container {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            margin-top: 16px;
        }

        .factor-bar-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 14px;
        }
        .factor-bar-row:last-child {
            margin-bottom: 0;
        }

        .factor-bar-label {
            font-size: 12.5px;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            font-weight: 500;
            width: 180px;
            flex-shrink: 0;
        }

        .factor-bar-track {
            flex: 1;
            background: #EEF1F5;
            border-radius: 4px;
            height: 22px;
            overflow: hidden;
            min-width: 100px;
        }

        .factor-bar-fill {
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);
            transition: width 0.6s ease;
        }

        .factor-bar-value {
            font-size: 12.5px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            width: 50px;
            text-align: right;
            flex-shrink: 0;
        }

        /* ============================================================
           FACTORES DENTRO DE CHART-CARD (variante con card)
           ============================================================ */
        .chart-card .factor-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 14px;
        }
        .chart-card .factor-row:last-child {
            margin-bottom: 0;
        }
        .chart-card .factor-label {
            font-size: 12px;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            font-weight: 500;
            width: 160px;
            flex-shrink: 0;
        }
        .chart-card .factor-track {
            flex: 1;
            background: #EEF1F5;
            border-radius: 4px;
            height: 20px;
            overflow: hidden;
            min-width: 100px;
        }
        .chart-card .factor-fill {
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);
            transition: width 0.6s ease;
        }
        .chart-card .factor-value {
            font-size: 12px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            width: 50px;
            text-align: right;
            flex-shrink: 0;
        }

        /* ============================================================
           CHART CARDS (Tarjetas de gráficos)
           ============================================================ */
        .chart-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            height: 100%;
        }
        .chart-card h3 {
            font-size: 14px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 18px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid #EEF1F5;
        }
        
                /* ============================================================
           CHART CARDS (Tarjetas de gráficos)
           ============================================================ */
        .chart-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 22px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            height: 100%;
        }
        .chart-card h3 {
            font-size: 14px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            margin: 0 0 18px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid #EEF1F5;
        }

        /* ============================================================
           BARRAS DE FACTORES (dentro de chart-card)
           ============================================================ */
        .factor-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 14px;
        }
        .factor-row:last-child {
            margin-bottom: 0;
        }

        .factor-label {
            font-size: 12px;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            font-weight: 500;
            width: 170px;
            flex-shrink: 0;
            text-align: left;
            line-height: 1.3;
        }

        .factor-track {
            flex: 1;
            background: #EEF1F5;
            border-radius: 4px;
            height: 20px;
            overflow: hidden;
            min-width: 80px;
            position: relative;
        }

        .factor-fill {
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);
            transition: width 0.6s ease;
            min-width: 2px;
        }

        .factor-value {
            font-size: 12px;
            font-weight: 700;
            color: #0B2440 !important;
            -webkit-text-fill-color: #0B2440 !important;
            width: 45px;
            text-align: right;
            flex-shrink: 0;
        }

        /* ============================================================
           NLP EVAL CARD (Métricas del modelo)
           ============================================================ */
        .nlp-eval-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 20px 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            border: 1px solid #E0E4EA;
        }
        .nlp-eval-item {
            text-align: center;
        }
        .nlp-eval-item .item-label {
            font-size: 10.5px;
            color: #666 !important;
            -webkit-text-fill-color: #666 !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .nlp-eval-item .item-value {
            font-size: 26px;
            font-weight: 700;
            color: #035AA6 !important;
            -webkit-text-fill-color: #035AA6 !important;
            line-height: 1;
        }
        .nlp-eval-item .item-value.verde {
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }
        .nlp-eval-item .item-check {
            font-size: 22px;
            color: #2E7D32 !important;
            -webkit-text-fill-color: #2E7D32 !important;
        }

        /* ============================================================
           COLORES DE SENTIMIENTO NETO EN TABLAS
           ============================================================ */
        .result-table td.sent-neto-positivo,
        .result-table td.sent-neto-positivo * {
            color: #15803D !important;
            -webkit-text-fill-color: #15803D !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .result-table td.sent-neto-negativo,
        .result-table td.sent-neto-negativo * {
            color: #DC2626 !important;
            -webkit-text-fill-color: #DC2626 !important;
            font-weight: 700 !important;
            text-align: right;
        }
        .result-table td.sent-neto-cero,
        .result-table td.sent-neto-cero * {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-weight: 600 !important;
            text-align: right;
        }

        /* ============================================================
           BARRA DE PROGRESO EN TABLAS (columna Distribución)
           ============================================================ */
        .tabla-barra-track {
            background: #EEF1F5;
            border-radius: 4px;
            height: 20px;
            overflow: hidden;
            width: 100%;
            position: relative;
        }
        .tabla-barra-fill {
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, #035AA6 0%, #3B7BBF 100%);
            transition: width 0.6s ease;
            min-width: 2px;
        }
        
    </style>
    """, unsafe_allow_html=True)