from typing import Dict, Any
from ..models.user_profile import UserProfile
from sqlalchemy.orm import Session
import json

class TranslationService:
    """Service for translating educational content based on user preferences"""
    
    # Simple mapping for demonstration - in production, would use a proper translation API
    TRANSLATION_MAP = {
        "en": {
            "Introduction to Physical AI": "Introduction to Physical AI",
            "Humanoid Robotics Overview": "Humanoid Robotics Overview", 
            "Embodied Cognition and AI": "Embodied Cognition and AI",
            "Locomotion and Movement Control": "Locomotion and Movement Control",
            "Perception Systems": "Perception Systems",
            "Manipulation and Dexterity": "Manipulation and Dexterity",
            "Human-Robot Interaction": "Human-Robot Interaction",
            "AI Learning in Physical Systems": "AI Learning in Physical Systems",
            "Applications and Ethics": "Applications and Ethics",
            "Future of Physical AI": "Future of Physical AI",
            "Building Your First Physical AI System": "Building Your First Physical AI System",
            "Case Studies": "Case Studies",
            "Brief overview and learning objectives for this section.": "Brief overview and learning objectives for this section.",
            "In-depth exploration of key concepts in this chapter.": "In-depth exploration of key concepts in this chapter.",
            "Real-world examples and applications of the concepts discussed.": "Real-world examples and applications of the concepts discussed.",
            "Quick assessment to reinforce learning.": "Quick assessment to reinforce learning.",
            "Recap of key points and preparation for the next chapter.": "Recap of key points and preparation for the next chapter."
        },
        "es": {
            "Introduction to Physical AI": "Introducción a la IA Física",
            "Humanoid Robotics Overview": "Visión General de la Robótica Humanoides", 
            "Embodied Cognition and AI": "Cognición Incorporada y IA",
            "Locomotion and Movement Control": "Control de Locomoción y Movimiento",
            "Perception Systems": "Sistemas de Percepción",
            "Manipulation and Dexterity": "Manipulación y Destreza",
            "Human-Robot Interaction": "Interacción Humano-Robot",
            "AI Learning in Physical Systems": "Aprendizaje de IA en Sistemas Físicos",
            "Applications and Ethics": "Aplicaciones y Ética",
            "Future of Physical AI": "Futuro de la IA Física",
            "Building Your First Physical AI System": "Construyendo Su Primer Sistema de IA Física",
            "Case Studies": "Estudios de Caso",
            "Brief overview and learning objectives for this section.": "Breve descripción general y objetivos de aprendizaje para esta sección.",
            "In-depth exploration of key concepts in this chapter.": "Exploración en profundidad de los conceptos clave en este capítulo.",
            "Real-world examples and applications of the concepts discussed.": "Ejemplos del mundo real y aplicaciones de los conceptos discutidos.",
            "Quick assessment to reinforce learning.": "Evaluación rápida para reforzar el aprendizaje.",
            "Recap of key points and preparation for the next chapter.": "Resumen de puntos clave y preparación para el próximo capítulo."
        },
        "ur": {  # Using English text as placeholder - would be Urdu in a real implementation
            "Introduction to Physical AI": "Introduction to Physical AI",
            "Humanoid Robotics Overview": "Humanoid Robotics Overview", 
            "Embodied Cognition and AI": "Embodied Cognition and AI",
            "Locomotion and Movement Control": "Locomotion and Movement Control",
            "Perception Systems": "Perception Systems",
            "Manipulation and Dexterity": "Manipulation and Dexterity",
            "Human-Robot Interaction": "Human-Robot Interaction",
            "AI Learning in Physical Systems": "AI Learning in Physical Systems",
            "Applications and Ethics": "Applications and Ethics",
            "Future of Physical AI": "Future of Physical AI",
            "Building Your First Physical AI System": "Building Your First Physical AI System",
            "Case Studies": "Case Studies",
            "Brief overview and learning objectives for this section.": "Brief overview and learning objectives for this section.",
            "In-depth exploration of key concepts in this chapter.": "In-depth exploration of key concepts in this chapter.",
            "Real-world examples and applications of the concepts discussed.": "Real-world examples and applications of the concepts discussed.",
            "Quick assessment to reinforce learning.": "Quick assessment to reinforce learning.",
            "Recap of key points and preparation for the next chapter.": "Recap of key points and preparation for the next chapter."
        }
    }
    
    @staticmethod
    def translate_text(text: str, target_language: str) -> str:
        """Translate text to the target language"""
        if target_language not in TranslationService.TRANSLATION_MAP:
            return text  # Return original text if language not supported
        
        # Return translated text if available, otherwise return original
        return TranslationService.TRANSLATION_MAP[target_language].get(text, text)
    
    @staticmethod
    def translate_content(content: dict, target_language: str) -> dict:
        """Translate educational content to the target language"""
        if target_language == "en":
            return content  # English is the default, no translation needed
        
        translated_content = content.copy()
        
        # Translate key fields
        if "title" in translated_content:
            translated_content["title"] = TranslationService.translate_text(
                translated_content["title"], 
                target_language
            )
        
        if "content" in translated_content:
            translated_content["content"] = TranslationService.translate_text(
                translated_content["content"], 
                target_language
            )
        
        if "description" in translated_content:
            translated_content["description"] = TranslationService.translate_text(
                translated_content["description"], 
                target_language
            )
        
        if "steps" in translated_content and isinstance(translated_content["steps"], list):
            for i, step in enumerate(translated_content["steps"]):
                translated_content["steps"][i] = TranslationService.translate_content(step, target_language)
        
        return translated_content
    
    @staticmethod
    def get_user_preferred_language(db: Session, user_id: str) -> str:
        """Get the preferred language for a user"""
        user_profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        if user_profile and user_profile.preferred_language:
            return user_profile.preferred_language
        return "en"  # Default to English