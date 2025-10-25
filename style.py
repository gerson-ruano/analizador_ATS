# style.py - Versión corregida
import streamlit as st

def aplicar_estilo_principal():
    """Aplica el estilo principal con fondo gradiente"""
    st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background: #667db6;
        background: -webkit-linear-gradient(to bottom, #667db6, #0082c8, #0082c8, #667db6);
        background: linear-gradient(to bottom, #667db6, #0082c8, #0082c8, #667db6);
        background-attachment: fixed;
    }
    
    /* Contenedor principal */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    .main-header {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .page-subtitle {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Sidebar - Fondo igual que el principal */
    section[data-testid="stSidebar"] {
        background: #667db6 !important;
        background: linear-gradient(to bottom, #667db6, #0082c8, #0082c8, #667db6) !important;
    }
    
    /* Tarjetas mejoradas */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    }
    
    .feature-card h2 {
        color: #2c3e50;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    .feature-card p, .feature-card li {
        color: #34495e;
        line-height: 1.6;
    }
    
    .feature-card ul {
        padding-left: 1.2rem;
    }
    
    .feature-card li {
        margin-bottom: 0.5rem;
    }
    
    /* Mejoras generales */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(45deg, #667db6, #0082c8);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    /* Asegurar que el contenido del sidebar sea legible */
    .css-1d391kg, .css-1lcbmhc {
        color: white;
    }
    
    .stSidebar .stMarkdown, .stSidebar .stTitle {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def crear_header(titulo, subtitulo=""):
    """Crea un header consistente"""
    st.markdown(f'<h1 class="main-header">{titulo}</h1>', unsafe_allow_html=True)
    if subtitulo:
        st.markdown(f'<p class="page-subtitle">{subtitulo}</p>', unsafe_allow_html=True)

def crear_tarjeta(titulo, contenido, icono="✅"):
    """Crea una tarjeta de características mejorada"""
    tarjeta_html = f"""
    <div class="feature-card">
        <h2>{icono} {titulo}</h2>
        <div>{contenido}</div>
    </div>
    """
    return st.markdown(tarjeta_html, unsafe_allow_html=True)