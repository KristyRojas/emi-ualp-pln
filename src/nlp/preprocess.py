import re
import unicodedata
import spacy
from spellchecker import SpellChecker

nlp = spacy.load("es_core_news_lg")
spell = SpellChecker(language="es")

class Preprocessor:
    def limpiar(self, texto):
        if not texto:
            return ""
        # Normalización Unicode
        texto = unicodedata.normalize("NFC", texto)
        # Minúsculas
        texto = texto.lower()
        # Eliminar URLs
        texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
        # Eliminar menciones y hashtags
        texto = re.sub(r'@\w+', '', texto)
        texto = re.sub(r'#\w+', '', texto)
        # Eliminar caracteres especiales (conservando tildes y ñ)
        texto = re.sub(r'[^a-záéíóúñ0-9\s]', '', texto)
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto).strip()
        # Corrección ortográfica básica (opcional, puede ser lento)
        # palabras = texto.split()
        # texto = " ".join([spell.correction(p) or p for p in palabras])
        return texto
    
    def tokenizar_y_lematizar(self, texto):
        doc = nlp(texto)
        tokens = [token.lemma_.lower() for token in doc 
                  if not token.is_stop and len(token.text) > 2]
        return tokens
    