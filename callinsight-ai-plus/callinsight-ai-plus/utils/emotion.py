# emotion.py - Текстовая модель для русского языка
from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        # Рассмотрите модель DeepPavlov для русского языка
        # или другую предобученную модель, указанную в поиске[citation:1]
        self.model = pipeline(
            "text-classification",
            model="cointegrated/rubert-tiny2-cedr-emotion-detection",  # Пример модели для русского языка
            top_k=None
        )
        self.emotion_map = {
            'sadness': 'грусть',
            'anger': 'гнев',
            'disgust': 'отвращение',
            'fear': 'страх',
            'joy': 'радость',
            'neutral': 'нейтрально',
            'surprise': 'удивление'
        }
    
    def analyze_emotion(self, text):
        if not text or len(text.strip()) == 0:
            return {"emotion_ru": "нейтрально", "score": 1.0}
        
        # Ограничим длину текста для модели
        results = self.model(text[:512])[0]
        
        # Возвращаем топ-эмоцию
        top_emotion = max(results, key=lambda x: x["score"])
        
        return {
            "emotion_eng": top_emotion["label"],
            "emotion_ru": self.emotion_map.get(top_emotion["label"], top_emotion["label"]),
            "score": round(top_emotion["score"], 3)
        }