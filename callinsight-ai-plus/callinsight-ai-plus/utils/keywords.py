# keywords.py - Исправленная версия
from yake import KeywordExtractor
import pymorphy2

class KeywordExtractorRU:
    def __init__(self):
        self.extractor = KeywordExtractor(
            lan="ru",
            n=3,  # Максимальная длина фразы
            dedupLim=0.9,
            top=10
        )
        self.morph = pymorphy2.MorphAnalyzer()
    
    def extract_keywords(self, text):
        if not text or len(text.strip()) < 20:
            return []
        
        # Извлекаем ключевые фразы
        keywords = self.extractor.extract_keywords(text)
        
        # Нормализуем слова (приводим к начальной форме)
        normalized_keywords = []
        for kw, score in keywords:
            words = kw.split()
            normalized_words = []
            for word in words:
                parsed = self.morph.parse(word)[0]
                normalized_words.append(parsed.normal_form)
            
            # Сохраняем нормализованную фразу и оценку
            normalized_phrase = " ".join(normalized_words)
            normalized_keywords.append((normalized_phrase, score))
        
        # Сортируем по оценке (чем меньше, тем лучше в YAKE)
        normalized_keywords.sort(key=lambda x: x[1])
        
        # Возвращаем только фразы (без оценок для удобства)
        return [kw for kw, _ in normalized_keywords[:10]]