import streamlit as st
import os

def navbar(current_page_name):
    """
    Navbar simplificado solo para navegación
    """
    
    PAGES = {
        "inicio": {"icon": "🏠", "label": "Inicio", "target": "inicio.py"},
        "mejorador": {"icon": "🔍", "label": "Mejorador de CV", "target": "pages/1_✨_mejorador_CV.py"},
        "analisis": {"icon": "✅", "label": "Analisis profundo", "target": "pages/2_📊_analisis_ATS.py"},
    }
    
    # Crear columnas para los botones
    columns = st.columns(len(PAGES))
    
    # Botones de navegación
    for i, (page_key, page_info) in enumerate(PAGES.items()):
        with columns[i]:
            is_active = current_page_name == page_key
            
            if st.button(
                f"{page_info['icon']} {page_info['label']}",
                help=page_info["label"],
                use_container_width=True,
                type="secondary" if is_active else "secondary"
            ):
                try:
                    st.switch_page(page_info["target"])
                except Exception as e:
                    st.error(f"Error al navegar: {e}")
    
    st.markdown("---")