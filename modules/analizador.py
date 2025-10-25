import re
import spacy 
from collections import Counter
from typing import List, Dict, Any

class CVAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("es_core_news_sm")
            self.spacy_available = True
        except OSError:
            self.nlp = None
            self.spacy_available = False
        
        # Lista expandida de habilidades
        self.habilidades_tecnicas = [
            'python', 'java', 'javascript', 'typescript', 'sql', 'mysql', 'postgresql',
            'mongodb', 'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'fastapi', 'spring', 'laravel', 'ruby', 'php', 'c#', 'c++',
            'go', 'rust', 'swift', 'kotlin', 'android', 'ios', 'linux', 'windows', 'macos',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
            'jenkins', 'ci/cd', 'devops', 'agile', 'scrum', 'kanban', 'jira', 'confluence',
            'machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'tableau', 'power bi', 'excel', 'word', 'powerpoint',
            'outlook', 'sharepoint', 'salesforce', 'sap', 'oracle', 'redes', 'seguridad',
            'criptografía', 'api', 'rest', 'graphql', 'microservicios', 'arquitectura'
        ]
        
        self.habilidades_blandas = [
            'liderazgo', 'trabajo en equipo', 'comunicación', 'resolución de problemas',
            'pensamiento crítico', 'creatividad', 'adaptabilidad', 'gestión del tiempo',
            'organización', 'planificación', 'negociación', 'persuasión', 'empatía',
            'trabajo bajo presión', 'autonomía', 'proactividad', 'colaboración',
            'atención al detalle', 'innovación', 'flexibilidad', 'resiliencia'
        ]
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extrae habilidades técnicas y blandas"""
        text_lower = text.lower()
        
        habilidades_encontradas = {
            'tecnicas': [],
            'blandas': [],
            'categorizadas': {}
        }
        
        # Buscar habilidades técnicas
        for habilidad in self.habilidades_tecnicas:
            if habilidad in text_lower:
                habilidades_encontradas['tecnicas'].append(habilidad)
        
        # Buscar habilidades blandas
        for habilidad in self.habilidades_blandas:
            if habilidad in text_lower:
                habilidades_encontradas['blandas'].append(habilidad)
        
        # Categorizar habilidades
        habilidades_encontradas['categorizadas'] = self._categorize_skills(habilidades_encontradas['tecnicas'])
        
        return habilidades_encontradas
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categoriza las habilidades técnicas"""
        categorias = {
            'lenguajes': [],
            'frameworks': [],
            'bases_datos': [],
            'herramientas': [],
            'cloud': [],
            'metodologias': []
        }
        
        categorias_map = {
            'lenguajes': ['python', 'java', 'javascript', 'typescript', 'ruby', 'php', 'c#', 'c++', 'go', 'rust', 'swift', 'kotlin'],
            'frameworks': ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'laravel'],
            'bases_datos': ['sql', 'mysql', 'postgresql', 'mongodb'],
            'herramientas': ['git', 'github', 'gitlab', 'jenkins', 'docker', 'kubernetes', 'jira', 'confluence'],
            'cloud': ['aws', 'azure', 'gcp'],
            'metodologias': ['agile', 'scrum', 'kanban', 'devops', 'ci/cd']
        }
        
        for skill in skills:
            for categoria, habilidades in categorias_map.items():
                if skill in habilidades:
                    categorias[categoria].append(skill)
                    break
        
        return {k: v for k, v in categorias.items() if v}
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extrae información de experiencia laboral"""
        text_lower = text.lower()
        
        # Patrones mejorados para experiencia
        experience_patterns = [
            r'(\d+)\s*años?\s*de\s*experiencia',
            r'experiencia\s*:\s*(\d+)\s*años?',
            r'(\d+)\s*años?\s*en\s*[a-z\s]+',
            r'más\s+de\s+(\d+)\s*años',
            r'(\d+)\+?\s*años?',
            r'(\d+)\s*años?\s*de\s*trayectoria'
        ]
        
        años_experiencia = 0  # ✅ Inicializar en 0 en lugar de None
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                numeros = []
                for match in matches:
                    if isinstance(match, tuple):
                        for m in match:
                            if m.isdigit():
                                numeros.append(int(m))
                    elif match.isdigit():
                        numeros.append(int(match))
                
                if numeros:
                    años_experiencia = max(numeros)
                    break
        
        # Extraer empresas usando spaCy si está disponible
        empresas = []
        if self.spacy_available:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ == "ORG" and len(ent.text.strip()) > 2:
                        empresas.append(ent.text.strip())
            except Exception:
                pass
        
        # Buscar fechas de experiencia
        fecha_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|actual)',
            r'desde\s*(\d{4})\s*hasta\s*(\d{4})',
            r'(\w+\s*\d{4})\s*[-–]\s*(\w+\s*\d{4}|presente)'
        ]
        
        periodos = []
        for pattern in fecha_patterns:
            periodos.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return {
            'años_experiencia': años_experiencia,  # ✅ Siempre será un número
            'empresas': list(set(empresas))[:8],  # Máximo 8 empresas únicas
            'periodos_encontrados': len(periodos),
            'tiene_experiencia': años_experiencia > 0 or len(empresas) > 0 or len(periodos) > 0
        }
    
    def extract_education(self, text: str) -> Dict[str, Any]:
        """Extrae información educativa"""
        text_lower = text.lower()
        
        niveles_educativos = {
            'bachiller': [],
            'pregrado': [],
            'posgrado': [],
            'certificaciones': []
        }
        
        # Patrones para niveles educativos
        patrones_educacion = {
            'bachiller': ['bachiller', 'bachillerato', 'secundaria', 'colegio'],
            'pregrado': ['licenciatura', 'grado', 'ingeniería', 'universidad', 'carrera', 'pregrado'],
            'posgrado': ['maestría', 'master', 'doctorado', 'phd', 'posgrado', 'especialización'],
            'certificaciones': ['certificación', 'certificado', 'diplomado', 'curso', 'bootcamp', 'capacitación']
        }
        
        for nivel, palabras in patrones_educacion.items():
            for palabra in palabras:
                if palabra in text_lower:
                    niveles_educativos[nivel].append(palabra)
        
        # Buscar instituciones educativas
        instituciones = []
        if self.spacy_available:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ == "ORG" and any(palabra in ent.text.lower() for palabra in ['universidad', 'instituto', 'escuela', 'colegio', 'academia']):
                        instituciones.append(ent.text)
            except Exception:
                pass
        
        return {
            'niveles': {k: len(v) for k, v in niveles_educativos.items() if v},
            'instituciones': list(set(instituciones))[:5],
            'total_niveles': sum(len(v) for v in niveles_educativos.values())
        }
    
    def extract_contact_info(self, text: str) -> Dict[str, List[str]]:
        """Extrae información de contacto"""
        # Patrones para emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        # Patrones para teléfonos
        phones = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        
        # Patrones para URLs (LinkedIn, portfolio, etc.)
        urls = re.findall(r'https?://[^\s]+', text)
        
        return {
            'emails': list(set(emails)),
            'telefonos': list(set(phones))[:3],
            'urls': list(set(urls))[:5]
        }
    
    def analyze_text_quality(self, text: str) -> Dict[str, Any]:
        """Analiza la calidad del texto del CV"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Calcular métricas de legibilidad básicas
        avg_sentence_length = len(words) / max(len(sentences), 1)
        avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
        
        # Palabras de acción (verbos fuertes)
        action_words = ['logré', 'lideré', 'desarrollé', 'implementé', 'mejoré', 
                       'optimicé', 'gestioné', 'coordiné', 'creé', 'diseñé']
        
        action_word_count = sum(1 for word in words if word.lower() in action_words)
        
        return {
            'total_palabras': len(words),
            'total_oraciones': len([s for s in sentences if s.strip()]),
            'longitud_promedio_oracion': round(avg_sentence_length, 1),
            'longitud_promedio_palabra': round(avg_word_length, 1),
            'palabras_accion': action_word_count,
            'densidad_palabras_accion': round(action_word_count / max(len(words), 1) * 100, 1)
        }