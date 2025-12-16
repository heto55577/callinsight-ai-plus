# sentiment.py
from transformers import pipeline
import numpy as np
from collections import Counter

class SentimentAnalyzer:
    """
    Анализатор тональности для русского языка
    """
    
    def __init__(self, model_name="seara/rubert-tiny2-russian-sentiment"):
        """
        Инициализация модели анализа тональности
        
        Args:
            model_name: название предобученной модели
        """
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=model_name,
                tokenizer=model_name
            )
            self.model_loaded = True
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            print("Используется простой анализатор на правилах")
            self.model_loaded = False
        
        # Словари для rule-based анализа (запасной вариант)
        self.positive_words = [
            "хорошо", "отлично", "прекрасно", "замечательно", "спасибо",
            "доволен", "довольна", "довольны", "супер", "отличный",
            "рекомендую", "понравилось", "удобно", "быстро", "качественно"
        ]
        
        self.negative_words = [
            "плохо", "ужасно", "кошмар", "недоволен", "недовольна",
            "недовольны", "жалоба", "проблема", "сломал", "не работает",
            "медленно", "долго", "дорого", "разочарован", "отвратительно"
        ]
    
    def analyze_sentiment_transformers(self, text):
        """
        Анализ тональности с помощью transformers
        
        Returns:
            dict: результат анализа
        """
        if not text or len(text.strip()) < 3:
            return {
                "label": "NEUTRAL",
                "score": 0.5,
                "sentiment_ru": "нейтрально"
            }
        
        try:
            # Ограничиваем длину текста для модели
            truncated_text = text[:512]
            
            result = self.analyzer(truncated_text)[0]
            
            # Маппинг на русские метки
            label_map = {
                "POSITIVE": "позитивный",
                "NEGATIVE": "негативный",
                "NEUTRAL": "нейтральный",
                "LABEL_0": "негативный",  # для некоторых моделей
                "LABEL_1": "позитивный"
            }
            
            return {
                "label": result["label"],
                "score": round(result["score"], 3),
                "sentiment_ru": label_map.get(result["label"], result["label"])
            }
            
        except Exception as e:
            print(f"Ошибка анализа тональности: {e}")
            return self.analyze_sentiment_rules(text)
    
    def analyze_sentiment_rules(self, text):
        """
        Rule-based анализ тональности (запасной вариант)
        """
        text_lower = text.lower()
        
        # Подсчет положительных и отрицательных слов
        pos_count = sum(1 for word in self.positive_words 
                       if word in text_lower)
        neg_count = sum(1 for word in self.negative_words 
                       if word in text_lower)
        
        total_words = len(text_lower.split())
        
        if total_words == 0:
            return {"label": "NEUTRAL", "score": 0.5, "sentiment_ru": "нейтральный"}
        
        # Вычисление скора
        score = (pos_count - neg_count) / max(total_words, 1)
        normalized_score = (score + 1) / 2  # Приводим к диапазону 0-1
        
        # Определение тональности
        if normalized_score > 0.6:
            sentiment = "позитивный"
            label = "POSITIVE"
        elif normalized_score < 0.4:
            sentiment = "негативный"
            label = "NEGATIVE"
        else:
            sentiment = "нейтральный"
            label = "NEUTRAL"
        
        return {
            "label": label,
            "score": round(normalized_score, 3),
            "sentiment_ru": sentiment,
            "pos_count": pos_count,
            "neg_count": neg_count,
            "method": "rule_based"
        }
    
    def analyze_sentiment(self, text):
        """
        Основной метод анализа тональности
        
        Returns:
            dict: результат анализа
        """
        if self.model_loaded:
            return self.analyze_sentiment_transformers(text)
        else:
            return self.analyze_sentiment_rules(text)
    
    def analyze_sentiment_timeline(self, segments, window_size=3):
        """
        Анализ тональности с временной шкалой
        
        Args:
            segments: список сегментов с текстом и временем
            window_size: размер окна для сглаживания
            
        Returns:
            list: тональность по времени
        """
        sentiment_timeline = []
        
        for i, segment in enumerate(segments):
            if 'text' in segment and segment['text'].strip():
                sentiment = self.analyze_sentiment(segment['text'])
                
                sentiment_point = {
                    'time': segment.get('start', i),
                    'text': segment['text'][:100],  # Ограничиваем длину
                    'sentiment': sentiment['sentiment_ru'],
                    'score': sentiment['score'],
                    'speaker': segment.get('speaker', 'unknown')
                }
                
                sentiment_timeline.append(sentiment_point)
        
        # Применяем скользящее среднее для сглаживания
        if len(sentiment_timeline) > window_size:
            smoothed_timeline = []
            
            for i in range(len(sentiment_timeline)):
                start = max(0, i - window_size // 2)
                end = min(len(sentiment_timeline), i + window_size // 2 + 1)
                
                window_scores = [s['score'] for s in sentiment_timeline[start:end]]
                avg_score = np.mean(window_scores)
                
                smoothed_point = sentiment_timeline[i].copy()
                smoothed_point['smoothed_score'] = round(avg_score, 3)
                
                # Определяем сглаженную тональность
                if avg_score > 0.6:
                    smoothed_point['smoothed_sentiment'] = 'позитивный'
                elif avg_score < 0.4:
                    smoothed_point['smoothed_sentiment'] = 'негативный'
                else:
                    smoothed_point['smoothed_sentiment'] = 'нейтральный'
                
                smoothed_timeline.append(smoothed_point)
            
            return smoothed_timeline
        
        return sentiment_timeline
    
    def get_sentiment_summary(self, sentiment_results):
        """
        Сводная статистика по тональности
        
        Returns:
            dict: статистика
        """
        if not sentiment_results:
            return {
                "overall_sentiment": "нейтральный",
                "overall_score": 0.5,
                "positive_percentage": 0,
                "negative_percentage": 0,
                "neutral_percentage": 100
            }
        
        # Подсчет тональностей
        sentiments = [r.get('sentiment_ru', 'нейтральный') 
                     for r in sentiment_results if isinstance(r, dict)]
        
        sentiment_counts = Counter(sentiments)
        total = len(sentiments) if sentiments else 1
        
        # Средний скор
        scores = [r.get('score', 0.5) for r in sentiment_results 
                 if isinstance(r, dict)]
        avg_score = np.mean(scores) if scores else 0.5
        
        # Определение общей тональности
        if avg_score > 0.6:
            overall = "позитивный"
        elif avg_score < 0.4:
            overall = "негативный"
        else:
            overall = "нейтральный"
        
        return {
            "overall_sentiment": overall,
            "overall_score": round(avg_score, 3),
            "positive_percentage": round(
                sentiment_counts.get("позитивный", 0) / total * 100, 1
            ),
            "negative_percentage": round(
                sentiment_counts.get("негативный", 0) / total * 100, 1
            ),
            "neutral_percentage": round(
                sentiment_counts.get("нейтральный", 0) / total * 100, 1
            ),
            "total_segments": total,
            "sentiment_distribution": dict(sentiment_counts)
        }


class AdvancedSentimentAnalyzer(SentimentAnalyzer):
    """
    Продвинутый анализатор тональности с анализом аспектов
    """
    
    def __init__(self):
        super().__init__()
        
        # Аспекты для анализа (можно расширить)
        self.aspects = {
            "качество": ["качество", "качественный", "надежность", "прочный"],
            "цена": ["цена", "стоимость", "дорого", "дешево", "бюджет"],
            "сервис": ["сервис", "обслуживание", "поддержка", "помощь"],
            "доставка": ["доставка", "доставили", "срок", "курьер"],
            "продукт": ["товар", "продукт", "упаковка", "комплектация"]
        }
    
    def analyze_aspect_sentiment(self, text):
        """
        Анализ тональности по аспектам
        
        Returns:
            dict: тональность по аспектам
        """
        aspect_sentiments = {}
        
        for aspect, keywords in self.aspects.items():
            # Проверяем наличие ключевых слов аспекта
            aspect_mentioned = any(keyword in text.lower() 
                                  for keyword in keywords)
            
            if aspect_mentioned:
                # Анализируем тональность контекста вокруг ключевых слов
                aspect_score = self._analyze_aspect_context(text, keywords)
                
                aspect_sentiments[aspect] = {
                    "mentioned": True,
                    "score": aspect_score,
                    "sentiment": self._score_to_sentiment(aspect_score)
                }
            else:
                aspect_sentiments[aspect] = {
                    "mentioned": False,
                    "score": 0.5,
                    "sentiment": "нейтральный"
                }
        
        return aspect_sentiments
    
    def _analyze_aspect_context(self, text, keywords, context_words=5):
        """
        Анализ тональности контекста вокруг ключевых слов
        """
        words = text.lower().split()
        scores = []
        
        for i, word in enumerate(words):
            if word in keywords:
                # Берем контекст вокруг ключевого слова
                start = max(0, i - context_words)
                end = min(len(words), i + context_words + 1)
                context = " ".join(words[start:end])
                
                # Анализируем тональность контекста
                sentiment = self.analyze_sentiment(context)
                scores.append(sentiment['score'])
        
        # Возвращаем средний скор, или нейтральный если не найдено
        return np.mean(scores) if scores else 0.5
    
    def _score_to_sentiment(self, score):
        """Конвертация скора в тональность"""
        if score > 0.6:
            return "позитивный"
        elif score < 0.4:
            return "негативный"
        else:
            return "нейтральный"


if __name__ == "__main__":
    # Тестирование анализатора тональности
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "Очень доволен покупкой, все работает отлично!",
        "Товар сломался через день, ужасное качество.",
        "Доставка была вовремя, но цена высоковата.",
        "Спасибо за помощь, оператор был очень вежлив."
    ]
    
    print("Тест анализа тональности:")
    print("-" * 50)
    
    for text in test_texts:
        result = analyzer.analyze_sentiment(text)
        print(f"Текст: {text[:50]}...")
        print(f"Тональность: {result['sentiment_ru']} (счет: {result['score']})")
        print("-" * 50)