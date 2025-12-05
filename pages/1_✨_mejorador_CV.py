import streamlit as st
from controllers.auth import require_page_auth, get_current_user, logout, require_auth
require_page_auth() 
user_info = get_current_user()
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.procesador import DocumentProcessor
from modules.mejorador_cv import CVImprovementAnalyzer
from components.navbar_superior import navbar

def main():
    st.set_page_config(
        page_title="Mejorador de CV - Análisis Profesional", 
        page_icon="✨", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    navbar("mejorador")
    
    # CSS personalizado para el mejorador
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #5D5D5D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .improvement-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .high-priority {
        border-left-color: #e74c3c;
        background-color: #ffeaea;
    }
    .medium-priority {
        border-left-color: #f39c12;
        background-color: #fff4e6;
    }
    .low-priority {
        border-left-color: #27ae60;
        background-color: #eafaf1;
    }
    .score-excellent { color: #27ae60; font-weight: bold; }
    .score-good { color: #f39c12; font-weight: bold; }
    .score-poor { color: #e74c3c; font-weight: bold; }
    .nav-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #2E86AB;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin: 0.5rem;
    }
    /* 🔵 ESTILO IDÉNTICO A INPUT FOCUS DE STREAMLIT */
    [data-testid="stFileUploader"]:has([data-testid*="FileName"]) {
        border: 2px solid #1f77b4 !important;
        background: white !important;
        box-shadow: 0 0 0 1px #1f77b4 !important;
        outline: none !important;
    }

    /* Hover state */
    [data-testid="stFileUploader"]:hover {
        border-color: #b4291f !important;
    }

    [data-testid="stFileUploader"]:has([data-testid*="FileName"]):hover {
        border-color: #b4291f !important;
    }

    /* Oculta TODO el contenido por defecto */
    [data-testid="stFileUploader"] section > * {
        display: none !important;
    }

    /* Muestra solo nuestro contenido personalizado */
    [data-testid="stFileUploader"] section:after {
        content: "📎 Agregar archivo" !important;
        display: block !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
        color: rgb(107, 114, 128) !important;
    }

    /* Cambiar texto cuando hay archivos */
    [data-testid="stFileUploader"]:has([data-testid*="FileName"]) section:after {
        content: "✅ Archivos listos para procesar" !important;
        color: #1f77b4 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">✨ Mejorador Profesional de CV</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analiza y mejora la forma, estructura y presentación de tu Curriculum Vitae</p>', unsafe_allow_html=True)

    st.header("📤 Sube tu CV")
        
    uploaded_file = st.file_uploader(
        "**Selecciona tu archivo**",
        type=['pdf', 'docx', 'txt'],
        help="Formatos soportados: PDF, Word (DOCX), Texto (TXT)"
    )
    
    # Sidebar específico para mejora de CV
    with st.sidebar:
        st.header("🎯 ¿Qué analizamos?")
        st.markdown("""
        - **🏗️ Estructura**: Organización y secciones
        - **📝 Contenido**: Calidad de escritura y verbos de acción  
        - **🎨 Formato**: Presentación y legibilidad
        - **✅ Completitud**: Información esencial
        - **💡 Recomendaciones**: Mejoras específicas
        """)
        
        st.markdown("---")
        st.header("💡 Consejos Rápidos")
        st.markdown("""
        - **Verbos de acción** al inicio de cada punto
        - **Logros cuantificables** con números
        - **Estructura clara** con secciones definidas
        - **Longitud ideal**: 300-800 palabras
        - **Formato limpio** y profesional
        """)
        
        st.markdown("---")
    
    # Contenido principal
    if uploaded_file:
        with st.spinner("🔍 Analizando tu CV para identificar áreas de mejora..."):
            # Procesar documento
            processor = DocumentProcessor()
            cv_text, success = processor.extract_text_from_uploaded_file(uploaded_file)
            
            if not success:
                st.error(f"❌ {cv_text}")
                return
            
            # Analizar mejora del CV
            improvement_analyzer = CVImprovementAnalyzer()
            improvement_report = improvement_analyzer.generate_improvement_report(cv_text)
        
        # Header con puntuación general
        overall_score = improvement_report['overall_score']
        
        # Determinar color y mensaje según puntuación
        if overall_score >= 80:
            score_class = "score-excellent"
            score_message = "¡Excelente! Tu CV tiene buena base"
        elif overall_score >= 60:
            score_class = "score-good"
            score_message = "Buen CV, pero puede mejorar"
        else:
            score_class = "score-poor"
            score_message = "Necesita mejoras significativas"
        
        # Mostrar puntuación general
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                <h2 style="margin: 0; font-size: 3rem;">{overall_score}/100</h2>
                <p style="margin: 0; font-size: 1.2rem;">{score_message}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Puntuaciones por categoría - CORREGIDO
        st.markdown("---")
        st.subheader("📊 Puntuación por Categorías")
        
        col1, col2, col3, col4 = st.columns(4)
        categories = improvement_report['category_scores']
        
        # Usar las claves correctas del diccionario
        with col1:
            score = categories.get('estructura', 0)
            color = "green" if score >= 70 else "orange" if score >= 50 else "red"
            st.metric("🏗️ Estructura", f"{score}/100", delta_color="off")
        
        with col2:
            score = categories.get('contenido', 0)
            color = "green" if score >= 70 else "orange" if score >= 50 else "red"
            st.metric("📝 Contenido", f"{score}/100", delta_color="off")
        
        with col3:
            score = categories.get('formato', 0)
            color = "green" if score >= 70 else "orange" if score >= 50 else "red"
            st.metric("🎨 Formato", f"{score}/100", delta_color="off")
        
        with col4:
            score = categories.get('completitud', 0)  # ✅ CORREGIDO: 'completitud' en lugar de 'completeness'
            color = "green" if score >= 70 else "orange" if score >= 50 else "red"
            st.metric("✅ Completitud", f"{score}/100", delta_color="off")
        
        # Gráfico de radar - CORREGIDO
        fig_radar = go.Figure()
        
        # Usar las mismas claves que en las métricas
        categories_list = ['estructura', 'contenido', 'formato', 'completitud']
        scores_list = [categories.get(cat, 0) for cat in categories_list]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores_list + [scores_list[0]],
            theta=categories_list + [categories_list[0]],
            fill='toself',
            fillcolor='rgba(46, 134, 171, 0.6)',
            line=dict(color='#2E86AB', width=2),
            name='Tu CV'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            showlegend=False,
            title=dict(
                text="<b>Análisis Detallado por Categoría</b>",
                x=0.5,
                font=dict(size=16)
            ),
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # RECOMENDACIONES DE MEJORA
        st.markdown("---")
        st.subheader("💡 Plan de Mejora para tu CV")
        
        recommendations = improvement_report['recommendations']
        priorities = improvement_report['improvement_priority']
        
        # Mostrar prioridades de mejora
        st.info(f"**🎯 Orden de Prioridad:** {', '.join(priorities)}")
        
        # Organizar recomendaciones por prioridad
        high_priority = [r for r in recommendations if r['priority'] == 'alta']
        medium_priority = [r for r in recommendations if r['priority'] == 'media']
        low_priority = [r for r in recommendations if r['priority'] == 'baja']
        
        # ALTA PRIORIDAD
        if high_priority:
            st.error("## 🚨 Mejoras Críticas (Alta Prioridad)")
            for i, rec in enumerate(high_priority, 1):
                st.markdown(f"""
                <div class="improvement-card high-priority">
                    <h4>🔴 {i}. {rec['message']}</h4>
                    <p><strong>💡 Sugerencia:</strong> {rec['suggestion']}</p>
                    <p><strong>📂 Categoría:</strong> {rec['category']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # MEDIA PRIORIDAD
        if medium_priority:
            st.warning("## ⚠️ Mejoras Importantes (Prioridad Media)")
            for i, rec in enumerate(medium_priority, 1):
                st.markdown(f"""
                <div class="improvement-card medium-priority">
                    <h4>🟡 {i}. {rec['message']}</h4>
                    <p><strong>💡 Sugerencia:</strong> {rec['suggestion']}</p>
                    <p><strong>📂 Categoría:</strong> {rec['category']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # BAJA PRIORIDAD
        if low_priority:
            st.success("## 💡 Optimizaciones (Prioridad Baja)")
            for i, rec in enumerate(low_priority, 1):
                st.markdown(f"""
                <div class="improvement-card low-priority">
                    <h4>🟢 {i}. {rec['message']}</h4>
                    <p><strong>💡 Sugerencia:</strong> {rec['suggestion']}</p>
                    <p><strong>📂 Categoría:</strong> {rec['category']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ANÁLISIS DETALLADO - CORREGIDO
        st.markdown("---")
        st.subheader("📈 Análisis Detallado por Categoría")
        
        # Crear pestañas para cada categoría
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Estructura", "📝 Contenido", "🎨 Formato", "✅ Completitud"])
        
        with tab1:
            structure = improvement_report['detailed_analysis']['structure']
            st.write("### Organización y Secciones")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**✅ Secciones Encontradas:**")
                for section in structure['sections_found']:
                    st.write(f"• {section['section'].title()} (línea {section['line_number']})")
                
                if structure['sections_missing']:
                    st.write("**❌ Secciones Faltantes:**")
                    for section in structure['sections_missing']:
                        st.write(f"• {section.title()}")
            
            with col2:
                st.write("**📊 Estadísticas:**")
                st.metric("Total de Palabras", structure['word_count'])
                st.metric("Líneas de Texto", structure['line_count'])
                st.metric("Párrafos", structure['paragraph_count'])
                
                # Evaluación de longitud
                if structure['word_count'] < 300:
                    st.warning("**📝 Muy corto:** Ideal 300-800 palabras")
                elif structure['word_count'] > 800:
                    st.warning("**📝 Muy extenso:** Considera resumir")
                else:
                    st.success("**📝 Longitud adecuada**")
        
        with tab2:
            content = improvement_report['detailed_analysis']['content']
            st.write("### Calidad del Contenido")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Verbos de Acción", content['action_verbs_count'])
                if content['action_verbs_count'] < 5:
                    st.error("Necesitas más verbos de acción")
                else:
                    st.success("Buen uso de verbos")
            
            with col2:
                st.metric("Palabras Débiles", content['weak_words_count'])
                if content['weak_words_count'] > 3:
                    st.error("Reduce palabras débiles")
                else:
                    st.success("Excelente")
            
            with col3:
                st.metric("Oraciones", content['sentence_count'])
                st.info("Variedad es clave")
            
            with col4:
                st.metric("Long. Prom. Oración", f"{content['avg_sentence_length']} palabras")
                if 10 <= content['avg_sentence_length'] <= 25:
                    st.success("Longitud ideal")
                else:
                    st.warning("Ajusta longitud")
            
            # Ejemplos de verbos de acción
            with st.expander("💪 Lista de Verbos de Acción Recomendados"):
                verbs_cols = st.columns(3)
                all_verbs = improvement_analyzer.action_verbs
                for i, col in enumerate(verbs_cols):
                    with col:
                        for verb in all_verbs[i*7:(i+1)*7]:
                            st.write(f"• {verb}")
        
        with tab3:
            formatting = improvement_report['detailed_analysis']['formatting']
            st.write("### Presentación y Formato")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Long. Prom. Línea", f"{formatting['avg_line_length']} chars")
                if formatting['avg_line_length'] > 80:
                    st.error("Líneas muy largas")
                else:
                    st.success("Longitud adecuada")
            
            with col2:
                st.metric("Líneas Largas", formatting['long_lines_count'])
                if formatting['long_lines_count'] > 5:
                    st.error("Divide líneas largas")
                else:
                    st.success("Buen formato")
            
            with col3:
                st.metric("Puntos con Viñetas", formatting['bullet_points_count'])
                if formatting['bullet_points_count'] < 3:
                    st.warning("Usa más viñetas")
                else:
                    st.success("Buen uso de viñetas")
            
            # Consejos de formato
            st.write("**🎨 Consejos de Formato:**")
            format_tips = [
                "Usa viñetas (•) para listar logros",
                "Mantén líneas bajo 80 caracteres",
                "Espacio entre secciones",
                "Fuente profesional y legible",
                "Encabezados claros y consistentes"
            ]
            
            for tip in format_tips:
                st.write(f"• {tip}")
        
        with tab4:
            completeness = improvement_report['detailed_analysis']['completeness']
            st.write("### Información Completa")
            
            # Información de contacto
            st.write("**📞 Información de Contacto:**")
            contact_cols = st.columns(4)
            contact_info = completeness['contact_info']
            
            contact_cols[0].metric("Email", "✅" if contact_info['has_email'] else "❌")
            contact_cols[1].metric("Teléfono", "✅" if contact_info['has_phone'] else "❌")
            contact_cols[2].metric("LinkedIn", "✅" if contact_info['has_linkedin'] else "❌")
            
            # Educación y experiencia
            st.write("**🎓 Educación y Experiencia:**")
            edu_exp_cols = st.columns(3)
            edu_info = completeness['education_info']
            exp_info = completeness['experience_info']
            
            edu_exp_cols[0].metric("Educación Superior", "✅" if edu_info['has_higher_education'] else "❌")
            edu_exp_cols[1].metric("Años Experiencia", "✅" if exp_info['years_experience'] > 0 else "❌")
            edu_exp_cols[2].metric("Logros Cuantificables", "✅" if exp_info['has_quantifiable_achievements'] else "❌")
            
            # Habilidades
            st.write("**🛠️ Habilidades:**")
            skills_cols = st.columns(2)
            skills_info = completeness['skills_info']
            
            skills_cols[0].metric("Habilidades Técnicas", "✅" if skills_info['has_technical_skills'] else "❌")
            skills_cols[1].metric("Habilidades Blandas", "✅" if skills_info['has_soft_skills'] else "❌")
        
        # PLANTILLAS Y EJEMPLOS
        st.markdown("---")
        st.subheader("📋 Recursos para Mejorar")
        
        with st.expander("🎯 Ejemplos de Mejora Práctica"):
            st.markdown("""
            ### ✨ Transforma tus Descripciones:
            
            **❌ Antes (Débil):**
            - "Ayudé en el desarrollo del proyecto"
            - "Fui parte del equipo de ventas" 
            - "Tuve responsabilidades en marketing"
            
            **✅ Después (Fuerte):**
            - "Lideré el desarrollo que incrementó eficiencia 30%"
            - "Coordiné equipo de ventas que superó objetivos 25%"
            - "Implementé estrategia de marketing que generó 500 leads"
            
            ### 📝 Estructura Ideal:
            1. **Información de Contacto** (completa y actualizada)
            2. **Resumen Profesional** (2-3 líneas impactantes)
            3. **Experiencia Laboral** (logros cuantificables)
            4. **Educación** (relevante para el puesto)
            5. **Habilidades** (técnicas y blandas específicas)
            6. **Certificaciones** (valor agregado)
            """)
        
        with st.expander("📊 Plantilla de CV Optimizado"):
            st.markdown("""
            ```markdown
            NOMBRE COMPLETO
            Email: tu.email@ejemplo.com | Tel: +34 600 000 000 | LinkedIn: linkedin.com/in/tuperfil
            
            RESUMEN PROFESIONAL
            [2-3 líneas que resuman tu valor único y experiencia clave]
            
            EXPERIENCIA LABORAL
            • Lideré [proyecto] que resultó en [beneficio cuantificable]
            • Implementé [sistema/proceso] mejorando [métrica] en [%]
            • Gestioné equipo de [número] personas logrando [resultado]
            
            EDUCACIÓN
            • [Título] - [Universidad] ([Año])
            • [Certificación relevante] - [Institución] ([Año])
            
            HABILIDADES TÉCNICAS
            • [Habilidad 1], [Habilidad 2], [Habilidad 3]
            • [Herramienta 1], [Herramienta 2], [Herramienta 3]
            
            HABILIDADES BLANDAS
            • Liderazgo, Comunicación, Resolución de Problemas
            ```
            """)
        
        # BOTÓN DE DESCARGA (simulado)
        st.markdown("---")
        st.download_button(
            label="📄 Descargar Reporte de Análisis",
            data=f"""
            REPORTE DE MEJORA DE CV
            Puntuación General: {overall_score}/100
            
            RECOMENDACIONES PRINCIPALES:
            {chr(10).join([f"- {rec['message']}" for rec in recommendations[:5]])}
            
            PUNTUACIONES POR CATEGORÍA:
            - Estructura: {categories.get('estructura', 0)}/100
            - Contenido: {categories.get('contenido', 0)}/100  
            - Formato: {categories.get('formato', 0)}/100
            - Completitud: {categories.get('completitud', 0)}/100
            """,
            file_name=f"reporte_mejora_cv.txt",
            mime="text/plain"
        )
    
    else:
        # PANTALLA DE BIENVENIDA
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## 🎯 ¿Por qué mejorar tu CV?
            
            Un CV optimizado puede aumentar tus posibilidades de entrevista hasta en un **40%**. 
            Nuestro analizador te ayuda a:
            
            - **🔍 Identificar debilidades** específicas en tu CV
            - **💡 Recibir recomendaciones** prácticas y accionables
            - **📊 Mejorar la estructura** y organización
            - **🎨 Optimizar el formato** para mejor legibilidad
            - **✅ Completar información** esencial
            
            ## 🚀 ¿Cómo funciona?
            
            1. **Sube tu CV** en cualquier formato (PDF, Word, Texto)
            2. **Recibe análisis instantáneo** con puntuación detallada
            3. **Implementa las mejoras** siguiendo nuestras recomendaciones
            4. **Descarga tu CV mejorado** con consejos específicos
            
            ## 📈 Beneficios:
            
            - **Análisis profesional** gratuito
            - **Recomendaciones personalizadas**
            - **Plan de mejora** paso a paso
            - **Ejemplos prácticos** de transformación
            """)
        
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
            st.info("""
            **💡 Tip Rápido:**
            Los reclutadores pasan solo 6-8 segundos revisando cada CV. 
            ¡Asegúrate de que el tuyo destaque!
            """)
            
            st.success("""
            **✅ Lista de Verificación:**
            - Verbos de acción ✓
            - Logros cuantificables ✓  
            - Estructura clara ✓
            - Información completa ✓
            - Formato profesional ✓
            """)

if __name__ == "__main__":
    main()