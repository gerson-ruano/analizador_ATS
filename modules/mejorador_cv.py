import re
import spacy
from typing import Dict, List, Any, Tuple
from collections import Counter

class CVImprovementAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("es_core_news_sm")
            self.spacy_available = True
        except OSError:
            self.nlp = None
            self.spacy_available = False
        
        # Palabras de acción recomendadas
        self.action_verbs = [
            'logré', 'lideré', 'desarrollé', 'implementé', 'mejoré', 'optimicé',
            'gestioné', 'coordiné', 'creé', 'diseñé', 'automaticé', 'reduje',
            'incrementé', 'solucioné', 'analicé', 'planifiqué', 'organicé',
            'supervisé', 'capacité', 'negocié', 'innové', 'autoricé', 'presidé'
        ]
        
        # Secciones esenciales de un CV
        self.essential_sections = [
            'información personal', 'experiencia laboral', 'educación',
            'habilidades', 'resumen profesional', 'logros', 'certificaciones'
        ]
        
        # Palabras débiles a evitar
        self.weak_words = [
            'ayudé', 'participé', 'colaboré', 'asistí', 'fui parte de',
            'tuve que', 'debía', 'intenté', 'traté de', 'quizás', 'tal vez'
        ]

    def analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analiza la estructura general del CV"""
        lines = text.split('\n')
        sections_found = []
        section_patterns = {
            'información personal': ['nombre', 'teléfono', 'email', 'dirección', 'linkedin'],
            'experiencia laboral': ['experiencia', 'laboral', 'trabajo', 'empleo', 'profesional'],
            'educación': ['educación', 'formación', 'estudios', 'académico', 'universidad'],
            'habilidades': ['habilidades', 'competencias', 'skills', 'tecnologías'],
            'resumen profesional': ['resumen', 'perfil', 'objetivo', 'profesional'],
            'logros': ['logros', 'achievements', 'resultados', 'reconocimientos'],
            'certificaciones': ['certificaciones', 'cursos', 'diplomas', 'certificates']
        }
        
        # Detectar secciones
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            for section, keywords in section_patterns.items():
                if any(keyword in line_lower for keyword in keywords) and len(line_lower) < 100:
                    sections_found.append({
                        'section': section,
                        'line': line.strip(),
                        'line_number': i + 1
                    })
                    break
        
        # Análisis de densidad
        word_count = len(text.split())
        line_count = len(lines)
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        return {
            'sections_found': sections_found,
            'sections_missing': [s for s in self.essential_sections if s not in [sec['section'] for sec in sections_found]],
            'word_count': word_count,
            'line_count': line_count,
            'paragraph_count': paragraph_count,
            'avg_words_per_line': word_count / max(line_count, 1),
            'structure_score': self._calculate_structure_score(sections_found, word_count)
        }

    def analyze_content_quality(self, text: str) -> Dict[str, Any]:
        """Analiza la calidad del contenido"""
        text_lower = text.lower()
        words = text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # Contar palabras de acción
        action_verbs_count = sum(1 for word in words if word.lower() in self.action_verbs)
        
        # Contar palabras débiles
        weak_words_count = sum(1 for word in words if word.lower() in self.weak_words)
        
        # Análisis de oraciones
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        avg_sentence_length = sum(sentence_lengths) / max(len(sentence_lengths), 1)
        
        # Densidad de keywords (simulada)
        professional_keywords = ['gestión', 'desarrollo', 'implementación', 'optimización', 'liderazgo']
        keyword_density = sum(1 for word in words if word.lower() in professional_keywords)
        
        return {
            'action_verbs_count': action_verbs_count,
            'weak_words_count': weak_words_count,
            'sentence_count': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'keyword_density': keyword_density,
            'content_score': self._calculate_content_score(action_verbs_count, weak_words_count, avg_sentence_length, keyword_density)
        }

    def analyze_formatting(self, text: str) -> Dict[str, Any]:
        """Analiza el formato y presentación"""
        lines = text.split('\n')
        
        # Analizar longitud de líneas
        line_lengths = [len(line) for line in lines if line.strip()]
        avg_line_length = sum(line_lengths) / max(len(line_lengths), 1)
        long_lines = sum(1 for length in line_lengths if length > 100)
        
        # Detectar uso de mayúsculas excesivas
        uppercase_lines = sum(1 for line in lines if line.strip() and line.upper() == line and len(line) > 10)
        
        # Detectar listas y bullet points
        bullet_points = sum(1 for line in lines if line.strip().startswith(('-', '•', '*', '·')))
        
        # Espacios en blanco excesivos
        empty_lines = sum(1 for line in lines if not line.strip())
        empty_line_ratio = empty_lines / max(len(lines), 1)
        
        return {
            'avg_line_length': round(avg_line_length, 1),
            'long_lines_count': long_lines,
            'uppercase_lines_count': uppercase_lines,
            'bullet_points_count': bullet_points,
            'empty_lines_ratio': round(empty_line_ratio, 2),
            'formatting_score': self._calculate_formatting_score(avg_line_length, long_lines, uppercase_lines, bullet_points, empty_line_ratio)
        }

    def analyze_data_completeness(self, text: str) -> Dict[str, Any]:
        """Analiza la completitud de los datos"""
        contact_info = self._extract_contact_info(text)
        education_info = self._extract_education_info(text)
        experience_info = self._extract_experience_info(text)
        skills_info = self._extract_skills_info(text)
        
        completeness_score = self._calculate_completeness_score(
            contact_info, education_info, experience_info, skills_info
        )
        
        return {
            'contact_info': contact_info,
            'education_info': education_info,
            'experience_info': experience_info,
            'skills_info': skills_info,
            'completeness_score': completeness_score,
            'missing_elements': self._identify_missing_elements(contact_info, education_info, experience_info, skills_info)
        }

    def _extract_contact_info(self, text: str) -> Dict[str, bool]:
        """Extrae y verifica información de contacto"""
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phones = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        linkedin = re.findall(r'linkedin\.com/in/[^\s]+', text.lower())
        
        return {
            'has_email': len(emails) > 0,
            'has_phone': len(phones) > 0,
            'has_linkedin': len(linkedin) > 0,
            'email_count': len(emails),
            'phone_count': len(phones)
        }

    def _extract_education_info(self, text: str) -> Dict[str, Any]:
        """Extrae información educativa"""
        text_lower = text.lower()
        
        education_keywords = {
            'universidad': ['universidad', 'university', 'facultad'],
            'grado': ['grado', 'licenciatura', 'bachiller', 'ingeniería'],
            'posgrado': ['maestría', 'master', 'doctorado', 'phd'],
            'certificaciones': ['certificación', 'certificado', 'diploma']
        }
        
        found_levels = {}
        for level, keywords in education_keywords.items():
            found_levels[level] = any(keyword in text_lower for keyword in keywords)
        
        # Detectar años de estudio
        year_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|actual)',
            r'(\d{4})\s*al\s*(\d{4})'
        ]
        
        education_periods = []
        for pattern in year_patterns:
            education_periods.extend(re.findall(pattern, text))
        
        return {
            'levels_found': found_levels,
            'education_periods': len(education_periods),
            'has_higher_education': found_levels['universidad'] or found_levels['grado'] or found_levels['posgrado']
        }

    def _extract_experience_info(self, text: str) -> Dict[str, Any]:
        """Extrae información de experiencia"""
        text_lower = text.lower()
        
        # Patrones para experiencia
        exp_patterns = [
            r'(\d+)\s*años?\s*de\s*experiencia',
            r'experiencia\s*:\s*(\d+)\s*años?',
            r'(\d+)\s*años?\s*en\s*[a-z\s]+'
        ]
        
        years_experience = 0
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                for match in matches:
                    if isinstance(match, tuple) and match[0].isdigit():
                        years_experience = max(years_experience, int(match[0]))
                    elif isinstance(match, str) and match.isdigit():
                        years_experience = max(years_experience, int(match))
        
        # Detectar empresas
        if self.spacy_available:
            try:
                doc = self.nlp(text)
                companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
            except:
                companies = []
        else:
            companies = []
        
        # Periodos laborales
        work_periods = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|actual)', text)
        
        return {
            'years_experience': years_experience,
            'companies_mentioned': len(companies),
            'work_periods': len(work_periods),
            'has_quantifiable_achievements': self._has_quantifiable_achievements(text)
        }

    def _extract_skills_info(self, text: str) -> Dict[str, Any]:
        """Extrae información de habilidades"""
        text_lower = text.lower()
        
        # Categorías de habilidades
        skill_categories = {
            'technical': ['python', 'java', 'sql', 'javascript', 'html', 'css', 'react', 'angular'],
            'soft': ['liderazgo', 'comunicación', 'trabajo en equipo', 'resolución de problemas'],
            'tools': ['git', 'docker', 'aws', 'azure', 'jenkins', 'jira']
        }
        
        skills_found = {}
        for category, skills in skill_categories.items():
            skills_found[category] = sum(1 for skill in skills if skill in text_lower)
        
        return {
            'skills_by_category': skills_found,
            'total_skills': sum(skills_found.values()),
            'has_technical_skills': skills_found['technical'] > 0,
            'has_soft_skills': skills_found['soft'] > 0
        }

    def _has_quantifiable_achievements(self, text: str) -> bool:
        """Verifica si hay logros cuantificables"""
        quantifiable_patterns = [
            r'increment[oó]\s+en\s+\d+%',
            r'reduj[eé]\s+en\s+\d+%',
            r'aument[oó]\s+de\s+\$?\d+',
            r'ahorr[oó]\s+\$?\d+',
            r'mejor[oó]\s+en\s+\d+%',
            r'\d+\s*%',
            r'\$\d+',
            r'\d+\s*(veces|times)'
        ]
        
        for pattern in quantifiable_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _identify_missing_elements(self, contact_info: Dict, education_info: Dict, experience_info: Dict, skills_info: Dict) -> List[str]:
        """Identifica elementos faltantes en el CV"""
        missing = []
        
        if not contact_info['has_email']:
            missing.append("Email de contacto")
        if not contact_info['has_phone']:
            missing.append("Número de teléfono")
        if not contact_info['has_linkedin']:
            missing.append("Perfil de LinkedIn")
        
        if not education_info['has_higher_education']:
            missing.append("Formación académica clara")
        
        if experience_info['years_experience'] == 0:
            missing.append("Años de experiencia especificados")
        if experience_info['companies_mentioned'] == 0:
            missing.append("Empresas anteriores mencionadas")
        if not experience_info['has_quantifiable_achievements']:
            missing.append("Logros cuantificables")
        
        if not skills_info['has_technical_skills']:
            missing.append("Habilidades técnicas específicas")
        if not skills_info['has_soft_skills']:
            missing.append("Habilidades blandas")
        
        return missing

    def _calculate_structure_score(self, sections_found: List[Dict], word_count: int) -> int:
        """Calcula puntuación de estructura"""
        score = 0
        
        # Puntos por secciones encontradas
        essential_sections = ['información personal', 'experiencia laboral', 'educación', 'habilidades']
        found_essential = sum(1 for section in sections_found if section['section'] in essential_sections)
        score += (found_essential / len(essential_sections)) * 40
        
        # Puntos por longitud adecuada
        if 300 <= word_count <= 800:
            score += 30
        elif 200 <= word_count < 300 or 800 < word_count <= 1200:
            score += 20
        else:
            score += 10
        
        # Puntos por organización general
        score += min(len(sections_found) * 5, 30)
        
        return min(score, 100)

    def _calculate_content_score(self, action_verbs: int, weak_words: int, avg_sentence_length: float, keyword_density: int) -> int:
        """Calcula puntuación de contenido"""
        score = 0
        
        # Puntos por palabras de acción
        score += min(action_verbs * 3, 30)
        
        # Penalización por palabras débiles
        score -= min(weak_words * 2, 20)
        score = max(score, 0)
        
        # Puntos por longitud de oraciones
        if 10 <= avg_sentence_length <= 25:
            score += 30
        elif 5 <= avg_sentence_length < 10 or 25 < avg_sentence_length <= 35:
            score += 15
        else:
            score += 5
        
        # Puntos por densidad de keywords
        score += min(keyword_density * 4, 20)
        
        return min(score, 100)

    def _calculate_formatting_score(self, avg_line_length: float, long_lines: int, uppercase_lines: int, bullet_points: int, empty_line_ratio: float) -> int:
        """Calcula puntuación de formato"""
        score = 100  # Empezar con puntuación perfecta
        
        # Penalización por líneas muy largas
        if avg_line_length > 80:
            score -= 20
        elif avg_line_length > 100:
            score -= 40
        
        # Penalización por líneas en mayúsculas
        score -= min(uppercase_lines * 5, 20)
        
        # Penalización por espacios en blanco excesivos
        if empty_line_ratio > 0.3:
            score -= 15
        
        # Bonificación por uso de bullet points
        score += min(bullet_points * 2, 10)
        
        return max(score, 0)

    def _calculate_completeness_score(self, contact_info: Dict, education_info: Dict, experience_info: Dict, skills_info: Dict) -> int:
        """Calcula puntuación de completitud"""
        score = 0
        
        # Información de contacto (30 puntos)
        contact_score = 0
        if contact_info['has_email']:
            contact_score += 10
        if contact_info['has_phone']:
            contact_score += 10
        if contact_info['has_linkedin']:
            contact_score += 10
        score += contact_score
        
        # Educación (20 puntos)
        if education_info['has_higher_education']:
            score += 20
        elif education_info['education_periods'] > 0:
            score += 10
        
        # Experiencia (30 puntos)
        experience_score = 0
        if experience_info['years_experience'] > 0:
            experience_score += 10
        if experience_info['companies_mentioned'] > 0:
            experience_score += 10
        if experience_info['has_quantifiable_achievements']:
            experience_score += 10
        score += experience_score
        
        # Habilidades (20 puntos)
        skills_score = 0
        if skills_info['has_technical_skills']:
            skills_score += 10
        if skills_info['has_soft_skills']:
            skills_score += 10
        score += skills_score
        
        return min(score, 100)

    def generate_improvement_report(self, text: str) -> Dict[str, Any]:
        """Genera un reporte completo de mejora"""
        structure = self.analyze_structure(text)
        content = self.analyze_content_quality(text)
        formatting = self.analyze_formatting(text)
        completeness = self.analyze_data_completeness(text)
        
        # Puntuación general
        overall_score = (
            structure['structure_score'] * 0.25 +
            content['content_score'] * 0.30 +
            formatting['formatting_score'] * 0.20 +
            completeness['completeness_score'] * 0.25
        )
        
        # Recomendaciones específicas
        recommendations = self._generate_recommendations(structure, content, formatting, completeness)
        
        return {
            'overall_score': round(overall_score, 1),
            'category_scores': {
                'estructura': structure['structure_score'],
                'contenido': content['content_score'],
                'formato': formatting['formatting_score'],
                'completitud': completeness['completeness_score']
            },
            'detailed_analysis': {
                'structure': structure,
                'content': content,
                'formatting': formatting,
                'completeness': completeness
            },
            'recommendations': recommendations,
            'improvement_priority': self._get_improvement_priority(structure, content, formatting, completeness)
        }

    def _generate_recommendations(self, structure: Dict, content: Dict, formatting: Dict, completeness: Dict) -> List[Dict]:
        """Genera recomendaciones específicas para mejorar el CV"""
        recommendations = []
        
        # Recomendaciones de estructura
        if structure['structure_score'] < 70:
            if structure['sections_missing']:
                recommendations.append({
                    'category': 'Estructura',
                    'priority': 'alta',
                    'message': f"Agrega las secciones faltantes: {', '.join(structure['sections_missing'])}",
                    'suggestion': "Organiza tu CV en secciones claras para mejorar la legibilidad"
                })
            
            if structure['word_count'] < 300:
                recommendations.append({
                    'category': 'Estructura',
                    'priority': 'media',
                    'message': "El CV es muy corto, considera agregar más detalles",
                    'suggestion': "Expande tus descripciones de experiencia y habilidades"
                })
            elif structure['word_count'] > 800:
                recommendations.append({
                    'category': 'Estructura',
                    'priority': 'media',
                    'message': "El CV es muy extenso, considera resumir",
                    'suggestion': "Mantén el CV en 1-2 páginas máximo, elimina información redundante"
                })
        
        # Recomendaciones de contenido
        if content['content_score'] < 70:
            if content['action_verbs_count'] < 5:
                recommendations.append({
                    'category': 'Contenido',
                    'priority': 'alta',
                    'message': "Usa más verbos de acción para describir tus logros",
                    'suggestion': f"Ejemplos: {', '.join(self.action_verbs[:5])}"
                })
            
            if content['weak_words_count'] > 3:
                recommendations.append({
                    'category': 'Contenido',
                    'priority': 'media',
                    'message': "Reduce el uso de palabras débiles",
                    'suggestion': f"Evita: {', '.join(self.weak_words[:3])}"
                })
        
        # Recomendaciones de formato
        if formatting['formatting_score'] < 70:
            if formatting['long_lines_count'] > 5:
                recommendations.append({
                    'category': 'Formato',
                    'priority': 'media',
                    'message': "Demasiadas líneas muy largas afectan la legibilidad",
                    'suggestion': "Divide las líneas en párrafos más cortos (60-80 caracteres)"
                })
            
            if formatting['bullet_points_count'] < 3:
                recommendations.append({
                    'category': 'Formato',
                    'priority': 'baja',
                    'message': "Considera usar más listas con viñetas",
                    'suggestion': "Las listas mejoran el escaneo visual del CV"
                })
        
        # Recomendaciones de completitud
        if completeness['completeness_score'] < 70:
            for missing in completeness['missing_elements'][:3]:
                recommendations.append({
                    'category': 'Completitud',
                    'priority': 'alta',
                    'message': f"Falta: {missing}",
                    'suggestion': "Esta información es esencial para los reclutadores"
                })
        
        return recommendations

    def _get_improvement_priority(self, structure: Dict, content: Dict, formatting: Dict, completeness: Dict) -> List[str]:
        """Determina las áreas de mejora prioritarias"""
        scores = {
            'Estructura': structure['structure_score'],
            'Contenido': content['content_score'],
            'Formato': formatting['formatting_score'],
            'Completitud': completeness['completeness_score']
        }
        
        # Ordenar por puntuación más baja (más necesidad de mejora)
        return sorted(scores.keys(), key=lambda x: scores[x])