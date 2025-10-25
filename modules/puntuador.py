import re
import spacy
from collections import Counter
from typing import List, Dict, Any

class ATSScorer:
    def __init__(self, job_description: str = ""):
        try:
            self.nlp = spacy.load("es_core_news_sm")
            self.spacy_available = True
        except OSError:
            self.nlp = None
            self.spacy_available = False
        
        self.job_description = job_description
        self.job_analysis = self._analyze_job_description(job_description)
        self.job_keywords = self.job_analysis['keywords']
        self.required_skills = self.job_analysis['required_skills']
        self.job_requirements = self.job_analysis['requirements']
    
    def _analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Analiza profundamente la descripción del puesto para extraer requisitos"""
        if not job_description.strip():
            return {
                'keywords': [],
                'required_skills': {},
                'requirements': {},
                'has_description': False
            }
        
        jd_lower = job_description.lower()
        
        # 1. Extraer keywords principales
        keywords = self._extract_job_keywords(job_description)
        
        # 2. Identificar habilidades requeridas
        required_skills = self._identify_required_skills(jd_lower)
        
        # 3. Extraer requisitos específicos
        requirements = self._extract_specific_requirements(jd_lower)
        
        # 4. Detectar nivel de seniority
        seniority = self._detect_seniority(jd_lower)
        
        # 5. Identificar industrias/áreas
        industries = self._identify_industries(jd_lower)
        
        return {
            'keywords': keywords,
            'required_skills': required_skills,
            'requirements': requirements,
            'seniority': seniority,
            'industries': industries,
            'has_description': True
        }
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extrae palabras clave específicas del puesto"""
        if not job_description.strip():
            return []
        
        if self.spacy_available:
            try:
                doc = self.nlp(job_description.lower())
                keywords = []
                
                # Extraer términos técnicos y específicos
                technical_terms = []
                for token in doc:
                    if (token.pos_ in ['NOUN', 'PROPN'] and 
                        len(token.text) > 3 and 
                        not token.is_stop):
                        technical_terms.append(token.lemma_.lower())
                
                # Extraer frases compuestas (bigrams)
                bigrams = []
                for i in range(len(doc) - 1):
                    if (doc[i].pos_ in ['NOUN', 'ADJ'] and 
                        doc[i+1].pos_ in ['NOUN', 'PROPN'] and
                        not doc[i].is_stop and not doc[i+1].is_stop):
                        bigram = f"{doc[i].text} {doc[i+1].text}"
                        bigrams.append(bigram.lower())
                
                # Combinar y priorizar
                all_terms = technical_terms + bigrams
                term_freq = Counter(all_terms)
                
                # Filtrar términos muy genéricos
                generic_terms = {'experiencia', 'trabajo', 'empresa', 'puesto', 'equipo'}
                filtered_terms = [term for term, count in term_freq.most_common(25) 
                                if term not in generic_terms]
                
                return filtered_terms
                
            except Exception as e:
                print(f"Error con spaCy en keywords: {e}")
        
        # Fallback básico
        return self._extract_keywords_basic(job_description)
    
    def _identify_required_skills(self, jd_lower: str) -> Dict[str, List[str]]:
        """Identifica habilidades específicamente requeridas"""
        skills_categories = {
            'lenguajes_programacion': {
                'keywords': ['python', 'java', 'javascript', 'typescript', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
                'found': []
            },
            'frameworks': {
                'keywords': ['react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'laravel', 'express'],
                'found': []
            },
            'bases_datos': {
                'keywords': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'sql server'],
                'found': []
            },
            'herramientas_devops': {
                'keywords': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'github', 'gitlab'],
                'found': []
            },
            'analisis_datos': {
                'keywords': ['machine learning', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'tableau', 'power bi'],
                'found': []
            },
            'metodologias': {
                'keywords': ['agile', 'scrum', 'kanban', 'devops', 'ci/cd'],
                'found': []
            },
            'habilidades_blandas': {
                'keywords': ['trabajo en equipo', 'comunicación', 'liderazgo', 'resolución de problemas', 'adaptabilidad', 'proactividad'],
                'found': []
            }
        }
        
        for category, data in skills_categories.items():
            for skill in data['keywords']:
                if skill in jd_lower:
                    data['found'].append(skill)
        
        # Devolver solo las categorías con habilidades encontradas
        return {category: data['found'] for category, data in skills_categories.items() if data['found']}
    
    def _extract_specific_requirements(self, jd_lower: str) -> Dict[str, Any]:
        """Extrae requisitos específicos como años de experiencia, educación, etc."""
        requirements = {}
        
        # Años de experiencia requeridos
        exp_patterns = [
            r'(\d+)\s*(\+)?\s*años?\s*de\s*experiencia',
            r'experiencia\s*de\s*(\d+)\s*años?',
            r'mínimo\s*de\s*(\d+)\s*años?',
            r'(\d+)\s*años?\s*en\s*puestos?\s*similares'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, jd_lower)
            if matches:
                for match in matches:
                    if isinstance(match, tuple) and match[0].isdigit():
                        requirements['años_experiencia'] = int(match[0])
                        break
                    elif isinstance(match, str) and match.isdigit():
                        requirements['años_experiencia'] = int(match)
                        break
        
        # Nivel educativo requerido
        education_levels = {
            'bachiller': ['bachiller', 'secundaria'],
            'tecnico': ['técnico', 'tecnólogo'],
            'pregrado': ['licenciatura', 'grado', 'ingeniería', 'universitario'],
            'posgrado': ['maestría', 'master', 'doctorado', 'postgrado']
        }
        
        for level, keywords in education_levels.items():
            if any(keyword in jd_lower for keyword in keywords):
                requirements['nivel_educativo'] = level
                break
        
        # Idiomas requeridos
        languages = ['inglés', 'español', 'francés', 'alemán', 'portugués']
        found_languages = [lang for lang in languages if lang in jd_lower]
        if found_languages:
            requirements['idiomas'] = found_languages
        
        # Tipo de contrato/jornada
        contract_types = ['tiempo completo', 'medio tiempo', 'remoto', 'presencial', 'híbrido']
        found_contracts = [ct for ct in contract_types if ct in jd_lower]
        if found_contracts:
            requirements['tipo_contrato'] = found_contracts
        
        return requirements
    
    def _detect_seniority(self, jd_lower: str) -> str:
        """Detecta el nivel de seniority del puesto"""
        junior_keywords = ['junior', 'trainee', 'principiante', 'entry level', 'recién graduado']
        senior_keywords = ['senior', 'experto', 'avanzado', 'lead', 'principal', 'arquitecto']
        mid_keywords = ['semi-senior', 'semi senior', 'mid-level', 'intermedio']
        
        if any(keyword in jd_lower for keyword in senior_keywords):
            return 'senior'
        elif any(keyword in jd_lower for keyword in mid_keywords):
            return 'mid-level'
        elif any(keyword in jd_lower for keyword in junior_keywords):
            return 'junior'
        else:
            return 'no especificado'
    
    def _identify_industries(self, jd_lower: str) -> List[str]:
        """Identifica industrias o áreas específicas"""
        industries = {
            'tecnologia': ['tecnología', 'software', 'it', 'sistemas', 'desarrollo'],
            'finanzas': ['finanzas', 'bancario', 'fintech', 'contabilidad'],
            'salud': ['salud', 'médico', 'farmacéutico', 'hospital'],
            'educacion': ['educación', 'académico', 'enseñanza', 'universidad'],
            'retail': ['retail', 'comercio', 'ventas', 'ecommerce'],
            'manufactura': ['manufactura', 'producción', 'industrial', 'fábrica']
        }
        
        found_industries = []
        for industry, keywords in industries.items():
            if any(keyword in jd_lower for keyword in keywords):
                found_industries.append(industry)
        
        return found_industries
    
    def _extract_keywords_basic(self, job_description: str) -> List[str]:
        """Método básico de extracción de keywords"""
        text = job_description.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = re.findall(r'\b[a-záéíóúñ]{4,}\b', text)
        
        stop_words = {
            'para', 'con', 'del', 'los', 'las', 'por', 'como', 'más', 'sus',
            'este', 'esta', 'esto', 'tiene', 'debe', 'puede', 'trabajo',
            'empresa', 'puesto', 'equipo', 'nuestro', 'nuestra', 'busca',
            'buscamos', 'responsable', 'encargado', 'funciones', 'tareas',
            'deben', 'deberá', 'necesario', 'importante', 'además', 'también'
        }
        
        filtered_words = [word for word in words if word not in stop_words]
        word_freq = Counter(filtered_words)
        
        return [word for word, count in word_freq.most_common(15)]
    
    def calculate_adaptive_score(self, cv_text: str, skills: Dict, experience: Dict, education: Dict, contact_info: Dict) -> Dict[str, Any]:
        """Calcula puntuación ADAPTADA específicamente al puesto"""
        cv_text_lower = cv_text.lower()
        
        if not self.job_analysis['has_description']:
            return self._calculate_generic_score(cv_text, skills, experience, education, contact_info)
        
        scores = {}
        
        # 1. Score de ADAPTACIÓN a requisitos específicos (35%)
        adaptation_score = self._calculate_adaptation_score(cv_text_lower, skills, experience, education)
        scores['adaptacion'] = adaptation_score
        
        # 2. Score de HABILIDADES REQUERIDAS (25%)
        required_skills_score = self._calculate_required_skills_score(skills)
        scores['habilidades_requeridas'] = required_skills_score
        
        # 3. Score de EXPERIENCIA ESPECÍFICA (20%)
        specific_experience_score = self._calculate_specific_experience_score(experience)
        scores['experiencia_especifica'] = specific_experience_score
        
        # 4. Score de KEYWORDS del puesto (15%)
        keyword_score = self._calculate_keyword_score(cv_text_lower)
        scores['keywords_puesto'] = keyword_score
        
        # 5. Score de COMPATIBILIDAD general (5%)
        compatibility_score = self._calculate_compatibility_score(experience, education)
        scores['compatibilidad'] = compatibility_score
        
        # Calcular score total adaptado
        weights = {
            'adaptacion': 0.35,
            'habilidades_requeridas': 0.25,
            'experiencia_especifica': 0.20,
            'keywords_puesto': 0.15,
            'compatibilidad': 0.05
        }
        
        total_score = sum(scores[category] * weight for category, weight in weights.items())
        
        return {
            'puntuacion_total': round(total_score, 1),
            'desglose_adaptado': scores,
            'analisis_puesto': self.job_analysis,
            'match_detallado': self._get_detailed_match(cv_text_lower, skills, experience, education),
            'recomendaciones_especificas': self._generate_job_specific_recommendations(total_score, scores, skills, experience, education)
        }
    
    def _calculate_adaptation_score(self, cv_text_lower: str, skills: Dict, experience: Dict, education: Dict) -> float:
        """Calcula qué tan bien se adapta el CV a los requisitos específicos"""
        score = 0
        max_score = 100
        
        # 1. Cumplimiento de años de experiencia requeridos
        required_exp = self.job_analysis['requirements'].get('años_experiencia')
        actual_exp = experience.get('años_experiencia', 0)
        
        if required_exp and actual_exp:
            if actual_exp >= required_exp:
                score += 30
            elif actual_exp >= required_exp * 0.7:  # 70% del requerido
                score += 20
            else:
                score += 10
        
        # 2. Match de nivel de seniority
        required_seniority = self.job_analysis['seniority']
        if required_seniority != 'no especificado':
            # Lógica simple de compatibilidad de seniority
            seniority_compatibility = {
                'junior': 10,
                'mid-level': 20,
                'senior': 30
            }
            score += seniority_compatibility.get(required_seniority, 15)
        
        # 3. Habilidades requeridas específicas
        required_skills_count = sum(len(skills) for skills in self.job_analysis['required_skills'].values())
        matched_skills_count = 0
        
        for category, required_skills in self.job_analysis['required_skills'].items():
            if category == 'habilidades_blandas':
                cv_skills = set(skills.get('blandas', []))
            else:
                cv_skills = set(skills.get('tecnicas', []))
            
            matched_skills_count += len([skill for skill in required_skills if skill in cv_skills])
        
        if required_skills_count > 0:
            skills_match_ratio = matched_skills_count / required_skills_count
            score += skills_match_ratio * 40
        
        return min(score, max_score)
    
    def _calculate_required_skills_score(self, skills: Dict) -> float:
        """Calcula score basado en habilidades específicamente requeridas"""
        if not self.job_analysis['required_skills']:
            return 50.0  # Score base si no hay habilidades específicas requeridas
        
        total_required = sum(len(skills) for skills in self.job_analysis['required_skills'].values())
        total_matched = 0
        
        for category, required_skills in self.job_analysis['required_skills'].items():
            if category == 'habilidades_blandas':
                cv_skills = set(skills.get('blandas', []))
            else:
                cv_skills = set(skills.get('tecnicas', []))
            
            for required_skill in required_skills:
                if required_skill in cv_skills:
                    total_matched += 1
        
        return (total_matched / total_required) * 100 if total_required > 0 else 0
    
    def _calculate_specific_experience_score(self, experience: Dict) -> float:
        """Calcula score basado en experiencia relevante para el puesto"""
        score = 0
        
        # Años de experiencia
        años = experience.get('años_experiencia', 0)
        required_exp = self.job_analysis['requirements'].get('años_experiencia')
        
        if required_exp:
            # Puntuación proporcional a los años requeridos
            if años >= required_exp:
                score += 60
            else:
                score += (años / required_exp) * 60
        else:
            # Sin requisito específico, valorar experiencia general
            score += min(años * 10, 60)
        
        # Empresas relevantes (simulación)
        empresas_count = len(experience.get('empresas', []))
        score += min(empresas_count * 5, 20)
        
        # Estabilidad laboral (simulada por periodos)
        periodos = experience.get('periodos_encontrados', 0)
        score += min(periodos * 4, 20)
        
        return min(score, 100)
    
    def _calculate_keyword_score(self, cv_text_lower: str) -> float:
        """Calcula score basado en keywords específicas del puesto"""
        if not self.job_analysis['keywords']:
            return 50.0
        
        matches = sum(1 for keyword in self.job_analysis['keywords'] if keyword in cv_text_lower)
        return (matches / len(self.job_analysis['keywords'])) * 100
    
    def _calculate_compatibility_score(self, experience: Dict, education: Dict) -> float:
        """Calcula compatibilidad general con el puesto"""
        score = 0
        
        # Compatibilidad de educación
        required_education = self.job_analysis['requirements'].get('nivel_educativo')
        if required_education:
            education_levels = {'bachiller': 1, 'tecnico': 2, 'pregrado': 3, 'posgrado': 4}
            actual_education_level = 0
            
            # Encontrar el nivel educativo más alto del candidato
            for nivel in education.get('niveles', {}):
                level_value = education_levels.get(nivel, 0)
                actual_education_level = max(actual_education_level, level_value)
            
            required_level = education_levels.get(required_education, 0)
            if actual_education_level >= required_level:
                score += 50
        
        # Compatibilidad de industria (simulada)
        industries_match = len(self.job_analysis['industries']) > 0
        if industries_match:
            score += 50
        
        return score
    
    def _calculate_generic_score(self, cv_text: str, skills: Dict, experience: Dict, education: Dict, contact_info: Dict) -> Dict[str, Any]:
        """Calcula puntuación genérica cuando no hay descripción de puesto"""
        # Tu scoring original aquí
        return {
            'puntuacion_total': 50.0,
            'desglose_adaptado': {},
            'analisis_puesto': {'has_description': False},
            'match_detallado': {},
            'recomendaciones_especificas': ["ℹ️ Agrega una descripción del puesto para un análisis más preciso"]
        }
    
    def _get_detailed_match(self, cv_text_lower: str, skills: Dict, experience: Dict, education: Dict) -> Dict[str, Any]:
        """Proporciona un match detallado entre CV y puesto"""
        match_details = {
            'habilidades_coincidentes': {},
            'habilidades_faltantes': {},
            'cumple_experiencia': False,
            'cumple_educacion': False,
            'keywords_coincidentes': []
        }
        
        # Habilidades coincidentes y faltantes
        for category, required_skills in self.job_analysis['required_skills'].items():
            if category == 'habilidades_blandas':
                cv_skills = set(skills.get('blandas', []))
            else:
                cv_skills = set(skills.get('tecnicas', []))
            
            coincidentes = [skill for skill in required_skills if skill in cv_skills]
            faltantes = [skill for skill in required_skills if skill not in cv_skills]
            
            if coincidentes:
                match_details['habilidades_coincidentes'][category] = coincidentes
            if faltantes:
                match_details['habilidades_faltantes'][category] = faltantes
        
        # Verificar experiencia
        required_exp = self.job_analysis['requirements'].get('años_experiencia')
        actual_exp = experience.get('años_experiencia', 0)
        match_details['cumple_experiencia'] = actual_exp >= required_exp if required_exp else True
        
        # Keywords coincidentes
        match_details['keywords_coincidentes'] = [
            kw for kw in self.job_analysis['keywords'] 
            if kw in cv_text_lower
        ]
        
        return match_details
    
    def _generate_job_specific_recommendations(self, total_score: float, scores: Dict, skills: Dict, experience: Dict, education: Dict) -> List[str]:
        """Genera recomendaciones específicas para el puesto"""
        recommendations = []
        
        # Análisis de habilidades faltantes
        for category, skills_list in self.job_analysis['required_skills'].items():
            cv_skills = skills.get('blandas', []) if category == 'habilidades_blandas' else skills.get('tecnicas', [])
            missing_skills = [skill for skill in skills_list if skill not in cv_skills]
            
            if missing_skills and len(missing_skills) <= 3:  # Solo mencionar si faltan pocas
                recommendations.append(f"🛠️ **Agrega {category.replace('_', ' ')}:** {', '.join(missing_skills)}")
        
        # Verificar experiencia requerida
        required_exp = self.job_analysis['requirements'].get('años_experiencia')
        actual_exp = experience.get('años_experiencia', 0)
        
        if required_exp and actual_exp < required_exp:
            recommendations.append(f"📈 **Experiencia insuficiente:** Se requieren {required_exp} años, tienes {actual_exp}")
        
        # Recomendaciones de keywords
        if scores['keywords_puesto'] < 70:
            missing_keywords = [kw for kw in self.job_analysis['keywords'][:5] if kw not in self._get_detailed_match("", skills, experience, education)['keywords_coincidentes']]
            if missing_keywords:
                recommendations.append(f"🔍 **Incluye estas palabras clave:** {', '.join(missing_keywords[:3])}")
        
        # Recomendación general basada en el score
        if total_score < 50:
            recommendations.append("🎯 **Necesita mejoras significativas** para este puesto específico")
        elif total_score < 70:
            recommendations.append("💡 **Buen ajuste, pero puede mejorar** la adaptación al puesto")
        else:
            recommendations.append("✅ **Excelente ajuste** para este puesto")
        
        return recommendations[:6]  # Máximo 6 recomendaciones