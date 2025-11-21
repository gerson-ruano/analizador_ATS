import streamlit as st
import os
from controllers.auth import logout, get_current_user

def navbar(current_page_name):
    """
    Navbar con manejo de roles y botón de Cerrar Sesión
    """
    user_info = get_current_user()
    user_role = user_info.get("rol", "usuario")

    # Menu base visible para todos
    PAGES = {
        "inicio": {"icon": "🏠", "label": "Inicio", "target": "inicio.py"},
        "mejorador": {"icon": "🔍", "label": "Mejorador de CV", "target": "pages/1_✨_mejorador_CV.py"},
    }

    # Agregar página solo para ADMIN
    if user_role in ["admin", "superadmin"]:
        PAGES["analisis"] = {
            "icon": "✅",
            "label": "Analisis profundo",
            "target": "pages/2_📊_analisis_ATS.py"
        }

    # +1 columna para botón logout
    columns = st.columns(len(PAGES) + 1)

    # Botones de navegación
    for i, (page_key, page_info) in enumerate(PAGES.items()):
        with columns[i]:
            is_active = current_page_name == page_key
            
            if st.button(
                f"{page_info['icon']} {page_info['label']}",
                help=page_info["label"],
                use_container_width=True,
                type="secondary"
            ):
                st.switch_page(page_info["target"])

    # BOTÓN DE CERRAR SESIÓN
    with columns[-1]:
        if st.button(
            "🚪 Cerrar sesión",
            help="Salir del sistema",
            use_container_width=True,
            type="primary"
        ):
            logout()

    st.markdown("---")