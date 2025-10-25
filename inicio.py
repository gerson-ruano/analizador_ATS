# pages/0_🏠_Inicio.py
import streamlit as st

st.set_page_config(
    page_title="Sistema de Análisis de CVs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # CSS personalizado para mejorar toda la aplicación
    # En pages/0_🏠_Inicio.py - Reemplaza todo el CSS con este:
    st.markdown("""
    <style>
        /* Fondo gradiente para toda la página */
        .stApp {
            background: #667db6;
            background: -webkit-linear-gradient(to bottom, #667db6, #0082c8, #0082c8, #667db6);
            background: linear-gradient(to bottom, #667db6, #0082c8, #0082c8, #667db6);
        }
        
        /* Contenedor principal con fondo semi-transparente */
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        /* Header principal */
        .main-header {
            font-size: 3rem;
            color: #555;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: bold;
            
        }
        
        /* Mejorar el sidebar de navegación */
        .css-1d391kg, .css-1lcbmhc {
            background-color: rgba(248, 249, 250, 0.9);
            backdrop-filter: blur(10px);
        }
        
        /* Estilo para los elementos del menú lateral */
        .css-1lcbmhc .eczjsme11 {
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .css-1lcbmhc .eczjsme11:hover {
            background-color: #2E86AB !important;
            color: white !important;
        }
        
        /* Estilo para la página activa */
        .css-1lcbmhc .eczjsme11[data-testid="stSidebarNavLink"]:has(a[aria-current="page"]) {
            background-color: #2E86AB !important;
            color: white !important;
            font-weight: bold;
        }
        
        /* Tarjetas de características con nuevo diseño */
        .feature-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 15px;
            color: #333;
            margin: 1rem 0;
            border: 2px solid rgba(102, 125, 182, 0.3);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }
        
        .feature-card h2 {
            color: #2E86AB;
            margin-bottom: 1rem;
        }
        
        .feature-card ul {
            color: #555;
        }
        
        /* Botones de navegación */
        .nav-button {
            background: linear-gradient(135deg, #2E86AB 0%, #0082c8 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: transform 0.3s;
            border: none;
            font-weight: bold;
        }
        
        .nav-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Mejorar las métricas */
        .stMetric {
            background: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid rgba(102, 125, 182, 0.2);
        }
        
        /* Expanders con fondo mejorado */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 10px !important;
        }
        
        /* Texto del subtítulo */
        .subtitle {
            color: white;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal con diseño mejorado
    st.markdown('<h1 class="main-header">🔍 Sistema Profesional de CVs</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">Dos herramientas especializadas para optimizar tu curriculum vitae</p>', unsafe_allow_html=True)
    
    # Guía de uso
    st.subheader("¿Cómo empezar?")
    
    guide_col1, guide_col2, guide_col3 = st.columns(3)
    
    with guide_col1:
        st.markdown("""
        ### 1. 🧭 Navega
        **Usa el menú lateral** para elegir tu herramienta:
        - **📊 Analisis ATS** para puestos específicos
        - **✨ Mejorador CV** para mejora general
        """)
    
    with guide_col2:
        st.markdown("""
        ### 2. 📤 Sube tu CV
        **Formatos soportados:**
        - PDF 📄
        - Word 📋  
        - Texto 📝
        """)
    
    with guide_col3:
        st.markdown("""
        ### 3. 🎯 Recibe análisis
        **Resultados instantáneos:**
        - Puntuación detallada
        - Recomendaciones específicas
        - Plan de mejora personalizado
        """)

    # Tarjetas de características
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>📊 Análisis ATS</h2>
            <p><strong>Optimiza tu CV para sistemas de filtrado automático</strong></p>
            <ul>
                <li>✅ Análisis por puesto específico</li>
                <li>✅ Detección de palabras clave</li>
                <li>✅ Puntuación ATS en tiempo real</li>
                <li>✅ Recomendaciones personalizadas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>✨ Mejorador de CV</h2>
            <p><strong>Mejora la forma, estructura y presentación</strong></p>
            <ul>
                <li>✅ Análisis de estructura</li>
                <li>✅ Optimización de contenido</li>
                <li>✅ Mejora de formato</li>
                <li>✅ Completitud de información</li>
            </ul>
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