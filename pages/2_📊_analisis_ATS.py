import streamlit as st
from controllers.auth import require_page_auth, get_current_user, require_role
user_info = get_current_user()
require_role(['admin'])
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.procesador import DocumentProcessor
from modules.analizador import CVAnalyzer
from modules.puntuador import ATSScorer
from modules.mejorador_cv import CVImprovementAnalyzer
from components.navbar_superior import navbar


def safe_get(dictionary, key, default=0):
    """Función segura para obtener valores de diccionarios"""
    value = dictionary.get(key, default)
    return value if value is not None else default

def safe_multiply(value, multiplier, default=0):
    """Multiplicación segura que maneja valores None"""
    if value is None:
        return default
    try:
        return value * multiplier
    except (TypeError, ValueError):
        return default

def main():
    st.set_page_config(
        page_title="Analizador de CVs ATS", 
        page_icon="📄", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    navbar("analisis")
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background-color: #b4291f;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
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
    
    st.markdown('<h1 class="main-header">📄 Analizador de CVs - ATS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Esta herramienta te ayuda a optimizar calificaciones utilizando el sistemas ATS (Applicant Tracking System) para filtrar candidatos.</p>', unsafe_allow_html=True)
    
    st.header("📤 Sube el CV")
        
    uploaded_file = st.file_uploader(
        "**Agrega el CV a analizar**",
        type=['pdf', 'docx', 'txt'],
        help="Formatos soportados: PDF, Word (DOCX), Texto (TXT)"
    )
    job_description = st.text_area(
        "**Descripción del puesto**",
        height=200,
        placeholder="Pega aquí la descripción del puesto para un análisis más preciso...",
        help="Cuanto más detallada sea la descripción, más preciso será el análisis"
    )
    # Ejemplo de descripción de puesto
    with st.expander("📝 Ver ejemplo de descripción de puesto"):
        st.code("""
        Estamos buscando un Desarrollador Python con:
        - 3+ años de experiencia en Python y Django
        - Conocimientos en bases de datos SQL y MongoDB
        - Experiencia con React o Vue.js
        - Conocimientos en Docker y AWS
        - Habilidades de trabajo en equipo y comunicación
        - Inglés intermedio-avanzado
        """, language="text")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 ¿Qué se analizará?")
        st.markdown("""
        - ✅ **Coincidencia con el puesto**
        - 🛠️ **Habilidades técnicas y blandas**
        - 💼 **Experiencia laboral**
        - 🎓 **Formación académica**
        - 📞 **Información de contacto**
        - ✍️ **Calidad del contenido**
        """)
    
    # Contenido principal
    if uploaded_file:
        with st.spinner("🔍 Analizando tu CV... Esto puede tomar unos segundos"):
            # Procesar documento
            processor = DocumentProcessor()
            cv_text, success = processor.extract_text_from_uploaded_file(uploaded_file)
            
            if not success:
                st.error(f"❌ {cv_text}")
                return
            
            # Obtener estadísticas del documento
            doc_stats = processor.get_document_stats(cv_text)
            
            # Analizar contenido del CV
            analyzer = CVAnalyzer()
            skills = analyzer.extract_skills(cv_text)
            experience = analyzer.extract_experience(cv_text)
            education = analyzer.extract_education(cv_text)
            contact_info = analyzer.extract_contact_info(cv_text)
            text_quality = analyzer.analyze_text_quality(cv_text)
            
            # Calcular puntuación ATS - USANDO EL NUEVO MÉTODO ADAPTATIVO
            scorer = ATSScorer(job_description)
            results = scorer.calculate_adaptive_score(cv_text, skills, experience, education, contact_info)
        
        # Mostrar resultados principales
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Tarjeta de puntuación principal
            st.subheader("🏆 Puntuación ATS")
            
            # Usar la puntuación correcta de manera segura
            score_total = safe_get(results, 'puntuacion_total', 0)
            
            # Gráfico de gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=score_total,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Score Total", 'font': {'size': 24}},
                delta={'reference': 70, 'increasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'red'},
                        {'range': [50, 70], 'color': 'yellow'},
                        {'range': [70, 100], 'color': 'green'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas rápidas - CORREGIDAS
            st.subheader("📈 Estadísticas Rápidas")
            
            # Obtener valores de manera segura
            tech_skills = len(safe_get(skills, 'tecnicas', []))
            soft_skills = len(safe_get(skills, 'blandas', []))
            exp_years = safe_get(experience, 'años_experiencia', 0)
            empresas_count = len(safe_get(experience, 'empresas', []))
            education_levels = safe_get(education, 'total_niveles', 0)
            word_count = safe_get(doc_stats, 'palabras', 0) if doc_stats else 0
            
            stats_data = {
                'Métrica': [
                    'Habilidades Técnicas',
                    'Habilidades Blandas', 
                    'Años de Experiencia',
                    'Empresas Detectadas',
                    'Niveles Educativos',
                    'Palabras en CV'
                ],
                'Valor': [
                    tech_skills,
                    soft_skills,
                    exp_years,
                    empresas_count,
                    education_levels,
                    word_count
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        with col2:
            # Pestañas para organización
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🛠️ Habilidades", "💼 Experiencia", "📊 Análisis", "📄 Contenido", "🎯 Match con Puesto", "✨ Mejorar CV"])
            
            with tab1:
                st.subheader("Habilidades Identificadas")
                
                # Habilidades técnicas categorizadas
                if safe_get(skills, 'categorizadas'):
                    st.write("**Habilidades Técnicas por Categoría:**")
                    for categoria, habilidades in skills['categorizadas'].items():
                        with st.expander(f"🔧 {categoria.replace('_', ' ').title()} ({len(habilidades)})"):
                            cols = st.columns(3)
                            for i, habilidad in enumerate(habilidades):
                                cols[i % 3].write(f"✅ {habilidad}")
                
                # Habilidades técnicas simples
                if safe_get(skills, 'tecnicas'):
                    st.write("**Todas las Habilidades Técnicas:**")
                    tech_cols = st.columns(4)
                    for i, skill in enumerate(skills['tecnicas'][:12]):  # Mostrar máximo 12
                        tech_cols[i % 4].write(f"• {skill}")
                
                # Habilidades blandas
                if safe_get(skills, 'blandas'):
                    st.write("**Habilidades Blandas:**")
                    soft_cols = st.columns(3)
                    for i, skill in enumerate(skills['blandas']):
                        soft_cols[i % 3].write(f"💬 {skill}")
            
            with tab2:
                st.subheader("Experiencia Laboral")
                
                exp_years = safe_get(experience, 'años_experiencia', 0)
                if exp_years > 0:
                    st.metric("Años de Experiencia", exp_years)
                else:
                    st.metric("Años de Experiencia", "No especificado")
                
                empresas = safe_get(experience, 'empresas', [])
                if empresas:
                    st.write("**Empresas Detectadas:**")
                    for i, empresa in enumerate(empresas[:6], 1):
                        st.write(f"{i}. 🏢 {empresa}")
                
                periodos = safe_get(experience, 'periodos_encontrados', 0)
                if periodos > 0:
                    st.write(f"**Periodos laborales identificados:** {periodos}")
            
            with tab3:
                st.subheader("Análisis Detallado")
                
                # Gráfico de scores por categoría - COMPLETAMENTE CORREGIDO
                if 'desglose_adaptado' in results and results['desglose_adaptado']:
                    # Usar el desglose adaptado si existe
                    scores_data = results['desglose_adaptado']
                    chart_title = "Puntuación por Categoría (Adaptado al Puesto)"
                elif 'desglose' in results and results['desglose']:
                    # Fallback al desglose original
                    scores_data = results['desglose']
                    chart_title = "Puntuación por Categoría"
                else:
                    # Si no hay desglose, crear uno básico - COMPLETAMENTE SEGURO
                    tech_skills_count = len(safe_get(skills, 'tecnicas', []))
                    exp_years = safe_get(experience, 'años_experiencia', 0)
                    education_levels = safe_get(education, 'total_niveles', 0)
                    email_count = len(safe_get(contact_info, 'emails', []))
                    word_count = safe_get(text_quality, 'total_palabras', 0)
                    
                    scores_data = {
                        'Habilidades': min(tech_skills_count * 5, 100),
                        'Experiencia': min(safe_multiply(exp_years, 10), 100),
                        'Educación': min(safe_multiply(education_levels, 15), 100),
                        'Contacto': min(email_count * 20, 100),
                        'Calidad': min(safe_multiply(word_count, 0.2), 100)  # word_count / 5
                    }
                    chart_title = "Puntuación Estimada por Categoría"
                
                scores_df = pd.DataFrame({
                    'Categoría': list(scores_data.keys()),
                    'Puntuación': list(scores_data.values())
                })
                
                fig_bar = px.bar(
                    scores_df, 
                    x='Categoría', 
                    y='Puntuación',
                    title=chart_title,
                    color='Puntuación',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Calidad del texto - CORREGIDO
                st.write("**Análisis de Calidad de Texto:**")
                quality_cols = st.columns(4)
                quality_cols[0].metric("Palabras", safe_get(text_quality, 'total_palabras', 0))
                quality_cols[1].metric("Oraciones", safe_get(text_quality, 'total_oraciones', 0))
                quality_cols[2].metric("Pal. Acción", safe_get(text_quality, 'palabras_accion', 0))
                density = safe_get(text_quality, 'densidad_palabras_accion', 0)
                quality_cols[3].metric("Densidad Acción", f"{density}%")
            
            with tab4:
                st.subheader("Información de Contacto y Educación")
                
                # Contacto - CORREGIDO
                emails = safe_get(contact_info, 'emails', [])
                telefonos = safe_get(contact_info, 'telefonos', [])
                urls = safe_get(contact_info, 'urls', [])
                
                if emails or telefonos or urls:
                    st.write("**Información de Contacto:**")
                    if emails:
                        st.write(f"📧 **Emails:** {', '.join(emails)}")
                    if telefonos:
                        st.write(f"📞 **Teléfonos:** {', '.join(telefonos[:2])}")
                    if urls:
                        st.write("🌐 **URLs:**")
                        for url in urls[:3]:
                            st.write(f"   • {url}")
                
                # Educación - CORREGIDO
                niveles = safe_get(education, 'niveles', {})
                instituciones = safe_get(education, 'instituciones', [])
                
                if niveles:
                    st.write("**Niveles Educativos Detectados:**")
                    for nivel, cantidad in niveles.items():
                        st.write(f"🎓 {nivel.title()}: {cantidad} menciones")
                
                if instituciones:
                    st.write("**Instituciones Educativas:**")
                    for institucion in instituciones:
                        st.write(f"🏫 {institucion}")
            
            with tab5:
                st.subheader("🎯 Análisis de Adaptación al Puesto")
                
                analisis_puesto = safe_get(results, 'analisis_puesto', {})
                
                if analisis_puesto.get('has_description'):
                    # Mostrar análisis del puesto
                    st.write("**📋 Requisitos del Puesto Detectados:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        requirements = safe_get(analisis_puesto, 'requirements', {})
                        exp_requerida = safe_get(requirements, 'años_experiencia')
                        if exp_requerida:
                            st.metric("Años de Experiencia Requeridos", exp_requerida)
                        
                        seniority = safe_get(analisis_puesto, 'seniority', 'no especificado')
                        if seniority != 'no especificado':
                            st.metric("Nivel de Seniority", seniority.title())
                    
                    with col2:
                        nivel_educativo = safe_get(requirements, 'nivel_educativo')
                        if nivel_educativo:
                            st.metric("Nivel Educativo Requerido", nivel_educativo.title())
                        
                        industries = safe_get(analisis_puesto, 'industries', [])
                        if industries:
                            st.write("**Industrias:**", ", ".join(industries))
                    
                    # Habilidades requeridas
                    required_skills = safe_get(analisis_puesto, 'required_skills', {})
                    if required_skills:
                        st.write("**🛠️ Habilidades Requeridas:**")
                        for category, skills_list in required_skills.items():
                            with st.expander(f"{category.replace('_', ' ').title()} ({len(skills_list)} habilidades)"):
                                for skill in skills_list:
                                    st.write(f"• {skill}")
                    
                    # Match detallado
                    match_details = safe_get(results, 'match_detallado', {})
                    st.write("**✅ Coincidencias Encontradas:**")
                    
                    habilidades_coincidentes = safe_get(match_details, 'habilidades_coincidentes', {})
                    if habilidades_coincidentes:
                        st.success("**Habilidades que coinciden:**")
                        for category, skills in habilidades_coincidentes.items():
                            st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")
                    
                    habilidades_faltantes = safe_get(match_details, 'habilidades_faltantes', {})
                    if habilidades_faltantes:
                        st.error("**Habilidades faltantes:**")
                        for category, skills in habilidades_faltantes.items():
                            st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")
                
                else:
                    st.info("ℹ️ Agrega una descripción del puesto para ver el análisis de adaptación específico")

            with tab6:  # Agregar esta nueva pestaña
                st.subheader("🛠️ Mejora de CV - Análisis de Forma y Estructura")
                
                if cv_text and not cv_text.startswith("Error"):
                    # Analizar mejora del CV
                    improvement_analyzer = CVImprovementAnalyzer()
                    improvement_report = improvement_analyzer.generate_improvement_report(cv_text)
                    
                    # Mostrar puntuación general de mejora
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Puntuación General", f"{improvement_report['overall_score']}/100")
                    with col2:
                        st.metric("Estructura", f"{improvement_report['category_scores']['estructura']}/100")
                    with col3:
                        st.metric("Contenido", f"{improvement_report['category_scores']['contenido']}/100")
                    with col4:
                        st.metric("Formato", f"{improvement_report['category_scores']['formato']}/100")
                    
                    # Gráfico de radar para categorías
                    categories = list(improvement_report['category_scores'].keys())
                    scores = list(improvement_report['category_scores'].values())
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=scores + [scores[0]],  # Cerrar el círculo
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='Puntuación por Categoría'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False,
                        title="Análisis por Categorías de Mejora",
                        height=400
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Recomendaciones de mejora
                    st.subheader("💡 Recomendaciones de Mejora")
                    
                    # Organizar por prioridad
                    high_priority = [r for r in improvement_report['recommendations'] if r['priority'] == 'alta']
                    medium_priority = [r for r in improvement_report['recommendations'] if r['priority'] == 'media']
                    low_priority = [r for r in improvement_report['recommendations'] if r['priority'] == 'baja']
                    
                    if high_priority:
                        st.error("**🚨 Mejoras de Alta Prioridad**")
                        for rec in high_priority:
                            with st.expander(f"🔴 {rec['message']}", expanded=True):
                                st.write(f"**Sugerencia:** {rec['suggestion']}")
                                st.write(f"**Categoría:** {rec['category']}")
                    
                    if medium_priority:
                        st.warning("**⚠️ Mejoras de Prioridad Media**")
                        for rec in medium_priority:
                            with st.expander(f"🟡 {rec['message']}"):
                                st.write(f"**Sugerencia:** {rec['suggestion']}")
                                st.write(f"**Categoría:** {rec['category']}")
                    
                    if low_priority:
                        st.info("**💡 Mejoras de Prioridad Baja**")
                        for rec in low_priority:
                            with st.expander(f"🔵 {rec['message']}"):
                                st.write(f"**Sugerencia:** {rec['suggestion']}")
                                st.write(f"**Categoría:** {rec['category']}")
                    
                    # Análisis detallado por categoría
                    st.subheader("📊 Análisis Detallado")
                    
                    detail_tab1, detail_tab2, detail_tab3, detail_tab4 = st.tabs(["🏗️ Estructura", "📝 Contenido", "🎨 Formato", "✅ Completitud"])
                    
                    with detail_tab1:
                        structure = improvement_report['detailed_analysis']['structure']
                        st.write("**Secciones Encontradas:**")
                        for section in structure['sections_found']:
                            st.write(f"✅ {section['section'].title()} (línea {section['line_number']})")
                        
                        if structure['sections_missing']:
                            st.write("**Secciones Faltantes:**")
                            for section in structure['sections_missing']:
                                st.write(f"❌ {section.title()}")
                        
                        st.write("**Estadísticas de Estructura:**")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Palabras", structure['word_count'])
                        col2.metric("Líneas", structure['line_count'])
                        col3.metric("Párrafos", structure['paragraph_count'])
                    
                    with detail_tab2:
                        content = improvement_report['detailed_analysis']['content']
                        st.write("**Calidad del Contenido:**")
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Verbos Acción", content['action_verbs_count'])
                        col2.metric("Palabras Débiles", content['weak_words_count'])
                        col3.metric("Oraciones", content['sentence_count'])
                        col4.metric("Long. Prom. Oración", content['avg_sentence_length'])
                        
                        if content['action_verbs_count'] < 5:
                            st.info("**💡 Tip:** Usa más verbos de acción como: " + ", ".join(improvement_analyzer.action_verbs[:5]))
                    
                    with detail_tab3:
                        formatting = improvement_report['detailed_analysis']['formatting']
                        st.write("**Análisis de Formato:**")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Long. Prom. Línea", formatting['avg_line_length'])
                        col2.metric("Líneas Largas", formatting['long_lines_count'])
                        col3.metric("Viñetas", formatting['bullet_points_count'])
                        
                        if formatting['long_lines_count'] > 5:
                            st.warning("**📏 Considera dividir líneas muy largas para mejor legibilidad**")
                    
                    with detail_tab4:
                        completeness = improvement_report['detailed_analysis']['completeness']
                        st.write("**Completitud de Información:**")
                        
                        # Información de contacto
                        st.write("**📞 Contacto:**")
                        contact_cols = st.columns(4)
                        contact_cols[0].write(f"Email: {'✅' if completeness['contact_info']['has_email'] else '❌'}")
                        contact_cols[1].write(f"Teléfono: {'✅' if completeness['contact_info']['has_phone'] else '❌'}")
                        contact_cols[2].write(f"LinkedIn: {'✅' if completeness['contact_info']['has_linkedin'] else '❌'}")
                        
                        # Educación y experiencia
                        st.write("**🎓 Educación y Experiencia:**")
                        edu_exp_cols = st.columns(3)
                        edu_exp_cols[0].write(f"Educación Superior: {'✅' if completeness['education_info']['has_higher_education'] else '❌'}")
                        edu_exp_cols[1].write(f"Años Experiencia: {'✅' if completeness['experience_info']['years_experience'] > 0 else '❌'}")
                        edu_exp_cols[2].write(f"Logros Cuantificables: {'✅' if completeness['experience_info']['has_quantifiable_achievements'] else '❌'}")
                    
                    # Plantillas y ejemplos
                    with st.expander("📋 Plantillas y Ejemplos de Mejora"):
                        st.markdown("""
                        ### 🎯 Ejemplos de Mejoras:
                        
                        **❌ Antes:** "Ayudé en el desarrollo del proyecto"
                        **✅ Después:** "Lideré el desarrollo del proyecto que incrementó la eficiencia en 30%"
                        
                        **❌ Antes:** "Fui parte del equipo de ventas"
                        **✅ Después:** "Coordiné el equipo de ventas que superó los objetivos en 25%"
                        
                        ### 📝 Estructura Recomendada:
                        1. **Información de Contacto** (nombre, teléfono, email, LinkedIn)
                        2. **Resumen Profesional** (2-3 líneas con tu valor único)
                        3. **Experiencia Laboral** (orden inverso cronológico)
                        4. **Educación** (títulos y certificaciones)
                        5. **Habilidades** (técnicas y blandas)
                        6. **Logros y Certificaciones** (opcional)
                        
                        ### 💡 Consejos de Formato:
                        - Usa **viñetas** para listar logros
                        - Mantén las **líneas cortas** (60-80 caracteres)
                        - Usa **verbos de acción** al inicio de cada punto
                        - **Cuantifica** tus logros con números y porcentajes
                        """)
                
                else:
                    st.info("📄 Sube un CV para analizar y obtener recomendaciones de mejora")
        
        # Sección de recomendaciones - CORREGIDA
        st.markdown("---")
        st.subheader("💡 Recomendaciones para Mejorar")
        
        # Usar las recomendaciones correctas de manera segura
        recomendaciones_especificas = safe_get(results, 'recomendaciones_especificas', [])
        recomendaciones_generales = safe_get(results, 'recomendaciones', [])
        
        if recomendaciones_especificas:
            recomendaciones = recomendaciones_especificas
        elif recomendaciones_generales:
            recomendaciones = recomendaciones_generales
        else:
            # Generar recomendaciones básicas si no hay
            recomendaciones = [
                "💡 Incluye más habilidades técnicas específicas",
                "📈 Destaca tus logros y resultados cuantificables", 
                "🎓 Menciona todas tus certificaciones y estudios",
                "📞 Asegúrate de incluir información de contacto completa"
            ]
        
        for i, recommendation in enumerate(recomendaciones[:8], 1):  # Máximo 8 recomendaciones
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{i}. {recommendation}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Palabras clave faltantes - CORREGIDO
        keywords_faltantes = safe_get(results, 'keywords_faltantes', [])
        if keywords_faltantes:
            st.subheader("🔍 Palabras Clave Faltantes")
            st.write("Considera incluir estas palabras en tu CV:")
            keyword_cols = st.columns(4)
            for i, keyword in enumerate(keywords_faltantes[:8]):
                keyword_cols[i % 4].write(f"📌 {keyword}")
        
        # Habilidades faltantes - CORREGIDO
        habilidades_faltantes = safe_get(results, 'habilidades_faltantes', {})
        if habilidades_faltantes:
            st.subheader("❌ Habilidades Requeridas Faltantes")
            for categoria, habilidades in habilidades_faltantes.items():
                with st.expander(f"🔧 {categoria.replace('_', ' ').title()} ({len(habilidades)} faltantes)"):
                    for habilidad in habilidades:
                        st.write(f"⚠️ {habilidad}")
        
        # Texto extraído (collapsible)
        with st.expander("📄 Ver Texto Extraído del CV"):
            st.text_area(
                "Contenido extraído", 
                cv_text, 
                height=300,
                key="cv_text_display"
            )
            
            # Estadísticas del documento - CORREGIDO
            if doc_stats:
                st.write("**Estadísticas del documento:**")
                stats_cols = st.columns(4)
                stats_cols[0].metric("Caracteres", safe_get(doc_stats, 'caracteres', 0))
                stats_cols[1].metric("Palabras", safe_get(doc_stats, 'palabras', 0))
                stats_cols[2].metric("Líneas", safe_get(doc_stats, 'lineas', 0))
                stats_cols[3].metric("Párrafos", safe_get(doc_stats, 'parrafos', 0))
    
    else:
        # Página de inicio cuando no hay archivo
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/136/136521.png", width=200)
            
            st.markdown("""
            - Esta herramienta te ayuda a Pre-calificar candidatos
            - Proporciona un análisis detallado de su CV 
            - Sugerencias para optimizar tu CV al puesto requerido
            - Utiliza formatos compatibles para los sistemas ATS ***(Applicant Tracking System)*** 
            
            ### 📋 ¿Cómo funciona?
            
            1. **Sube tu CV** en formato PDF, Word o TXT
            2. **Pega la descripción** del puesto que te interesa
            3. **Obtén un análisis detallado** con puntuación y recomendaciones
                """)
        
        with col2:
            st.info("""
            ### 🎯 ¿Qué analizamos?
        
            | Área | Métricas |
            |------|----------|
            | **🔍 Coincidencia** | Palabras clave, habilidades requeridas |
            | **🛠️ Habilidades** | Técnicas, blandas, categorización |
            | **💼 Experiencia** | Años, empresas, periodos laborales |
            | **🎓 Educación** | Niveles, instituciones, certificaciones |
            | **📞 Contacto** | Emails, teléfonos, URLs profesionales |
            | **✍️ Calidad** | Estructura, verbos de acción, legibilidad |
                """)
            
            ### 💡 Consejos para un CV ATS-friendly:
            st.success("""
            - Usa **palabras clave** específicas de la industria
            - Incluye **habilidades técnicas** relevantes
            - Cuantifica tus **logros y resultados**
            - Mantén un **formato simple y legible**
            - Incluye **información de contacto** completa
                """)

if __name__ == "__main__":
    main()