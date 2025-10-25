# pages/0_🏠_Inicio.py - Versión mejorada
import streamlit as st
from style import aplicar_estilo_principal, crear_header, crear_tarjeta
from components.navbar_superior import navbar

st.set_page_config(
    page_title="Sistema de Análisis de CVs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Aplicar estilos reutilizables
    aplicar_estilo_principal()

    navbar("inicio")
    
    # Crear header consistente
    crear_header(
        "🔍 Sistema Profesional de CVs", 
        "Dos herramientas especializadas para optimizar tu curriculum vitae"
    )
    
    # Contenedor principal para mejor organización
    with st.container():
        # Tarjetas de características usando la función reutilizable
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            crear_tarjeta(
                "Análisis ATS",
                """
                <p><strong>Optimiza tu CV para sistemas de filtrado automático</strong></p>
                <ul>
                    <li>Análisis por puesto específico</li>
                    <li>Detección de palabras clave</li>
                    <li>Puntuación ATS en tiempo real</li>
                    <li>Recomendaciones personalizadas</li>
                </ul>
                """,
                "📊"
            )
        
        with col2:
            crear_tarjeta(
                "Mejorador de CV",
                """
                <p><strong>Mejora la forma, estructura y presentación</strong></p>
                <ul>
                    <li>Análisis de estructura</li>
                    <li>Optimización de contenido</li>
                    <li>Mejora de formato</li>
                    <li>Completitud de información</li>
                </ul>
                """,
                "✨"
            )
    
    # Guía de uso
    st.markdown("---")
    st.subheader("🎮 ¿Cómo empezar?")
    
    guide_col1, guide_col2, guide_col3 = st.columns(3)
    
    with guide_col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h3>1. 🧭 Navega</h3>
            <p><strong>Usa el menú lateral</strong> para elegir tu herramienta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with guide_col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h3>2. 📤 Sube tu CV</h3>
            <p><strong>Formatos soportados:</strong></p>
            <p>PDF 📄 • Word 📋 • Texto 📝</p>
        </div>
        """, unsafe_allow_html=True)
    
    with guide_col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h3>3. 🎯 Recibe análisis</h3>
            <p><strong>Resultados instantáneos</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Estadísticas
    st.markdown("---")
    st.subheader("📈 Resultados Comprobados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🚀 Eficiencia", "+40%", "más entrevistas")
    
    with col2:
        st.metric("🎯 Precisión", "85%", "de efectividad")
    
    with col3:
        st.metric("💼 Respuestas", "3.2x", "más respuestas")

if __name__ == "__main__":
    main()