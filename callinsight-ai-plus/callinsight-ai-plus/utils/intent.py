# intent.py
import re
from collections import Counter

class IntentDetector:
    """
    Детектор намерений для телефонных звонков
    """
    
    def __init__(self):
        # Паттерны для определения намерений
        self.intent_patterns = {
            "жалоба": [
                r"жалуюсь", r"жалоба", r"недоволен", r"проблема",
                r"сломал", r"не работает", r"возврат", r"претензия",
                r"плохой", r"ужасный", r"кошмар"
            ],
            "консультация": [
                r"подскажите", r"посоветуйте", r"вопрос", r"интересуюсь",
                r"хочу узнать", r"можно спросить", r"как использовать",
                r"инструкция", r"помогите разобраться"
            ],
            "заказ": [
                r"хочу заказать", r"куплю", r"оформить заказ",
                r"доставка", r"цена", r"сколько стоит", r"приобрести",
                r"доставите", r"оплата"
            ],
            "поддержка": [
                r"помощь", r"поддержка", r"не могу", r"не получается",
                r"что делать", r"как быть", r"решить проблему",
                r"техническая помощь"
            ],
            "отмена": [
                r"отменить", r"отмена", r"передумал", r"не хочу",
                r"вернуть", r"аннулировать", r"отказ"
            ],
            "статус": [
                r"статус", r"где мой", r"когда придет", r"отследить",
                r"номер заказа", r"ожидание", r"проверить"
            ],
            "сотрудничество": [
                r"сотрудничество", r"партнерство", r"оптом",
                r"скидка", r"договор", r"сотрудничать"
            ]
        }
        
        # Веса намерений (какие более важные)
        self.intent_weights = {
            "жалоба": 1.5,      # Жалобы самые важные
            "отмена": 1.3,      # Отмена заказа важна
            "поддержка": 1.2,    # Техподдержка
            "заказ": 1.0,
            "консультация": 0.9,
            "статус": 0.8,
            "сотрудничество": 0.7
        }
        
        # Ключевые слова для каждого намерения
        self.intent_keywords = {
            "жалоба": ["брак", "неисправность", "возврат", "претензия", "жалоба"],
            "консультация": ["как", "подскажите", "вопрос", "интересно"],
            "заказ": ["заказ", "доставка", "оплата", "цена", "купить"],
            "поддержка": ["помощь", "не работает", "ошибка", "исправить"],
            "отмена": ["отмена", "вернуть", "передумал", "аннулировать"],
            "статус": ["статус", "где", "когда", "отследить"],
            "сотрудничество": ["оптом", "партнер", "сотрудничество", "скидка"]
        }
    
    def detect_intent_patterns(self, text):
        """
        Определение намерений по паттернам
        
        Returns:
            dict: намерения с оценками
        """
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    # Учитываем количество совпадений
                    score += len(matches) * 0.1
                    # Бонус за точное совпадение
                    score += 0.05
            
            if score > 0:
                # Применяем вес намерения
                weighted_score = score * self.intent_weights.get(intent, 1.0)
                intent_scores[intent] = round(weighted_score, 3)
        
        return intent_scores
    
    def detect_intent_keywords(self, text):
        """
        Определение намерений по ключевым словам
        
        Returns:
            dict: намерения с оценками
        """
        words = text.lower().split()
        word_counts = Counter(words)
        
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = 0
            
            for keyword in keywords:
                if keyword in word_counts:
                    # Учитываем частоту ключевых слов
                    score += word_counts[keyword] * 0.15
            
            if score > 0:
                weighted_score = score * self.intent_weights.get(intent, 1.0)
                intent_scores[intent] = round(weighted_score, 3)
        
        return intent_scores
    
    def detect_intent_combined(self, text):
        """
        Комбинированное определение намерений
        
        Returns:
            dict: основное намерение и все оценки
        """
        # Получаем оценки разными методами
        pattern_scores = self.detect_intent_patterns(text)
        keyword_scores = self.detect_intent_keywords(text)
        
        # Объединяем оценки
        all_intents = set(list(pattern_scores.keys()) + list(keyword_scores.keys()))
        combined_scores = {}
        
        for intent in all_intents:
            pattern_score = pattern_scores.get(intent, 0)
            keyword_score = keyword_scores.get(intent, 0)
            
            # Среднее с небольшим смещением к паттернам
            combined_score = (pattern_score * 0.6 + keyword_score * 0.4)
            combined_scores[intent] = round(combined_score, 3)
        
        # Находим основное намерение
        if combined_scores:
            main_intent = max(combined_scores.items(), key=lambda x: x[1])
            main_intent_name = main_intent[0]
            main_intent_score = main_intent[1]
        else:
            main_intent_name = "неизвестно"
            main_intent_score = 0
        
        # Определяем уверенность
        if main_intent_score > 0.3:
            confidence = "высокая"
        elif main_intent_score > 0.15:
            confidence = "средняя"
        else:
            confidence = "низкая"
            main_intent_name = "неопределено"
        
        return {
            "main_intent": main_intent_name,
            "main_intent_score": main_intent_score,
            "confidence": confidence,
            "all_intents": combined_scores,
            "pattern_scores": pattern_scores,
            "keyword_scores": keyword_scores
        }
    
    def detect_intent_segments(self, segments):
        """
        Определение намерений по сегментам диалога
        
        Args:
            segments: список сегментов с текстом
            
        Returns:
            dict: намерения по сегментам и общие
        """
        segment_intents = []
        
        for i, segment in enumerate(segments):
            if 'text' in segment and segment['text'].strip():
                text = segment['text']
                intent_result = self.detect_intent_combined(text)
                
                segment_intent = {
                    'segment_id': i,
                    'speaker': segment.get('speaker', 'unknown'),
                    'start_time': segment.get('start', 0),
                    'text_preview': text[:100] + "..." if len(text) > 100 else text,
                    'main_intent': intent_result['main_intent'],
                    'intent_score': intent_result['main_intent_score'],
                    'confidence': intent_result['confidence']
                }
                
                segment_intents.append(segment_intent)
        
        # Определяем общее намерение звонка
        if segment_intents:
            # Учитываем только намерения с высокой уверенностью
            high_confidence_intents = [
                si for si in segment_intents 
                if si['confidence'] == 'высокая'
            ]
            
            if high_confidence_intents:
                # Берем самое частое намерение с высокой уверенностью
                intent_counts = Counter([si['main_intent'] 
                                       for si in high_confidence_intents])
                overall_intent = intent_counts.most_common(1)[0][0]
            else:
                # Или самое частое среди всех
                intent_counts = Counter([si['main_intent'] 
                                       for si in segment_intents])
                overall_intent = intent_counts.most_common(1)[0][0]
        else:
            overall_intent = "неопределено"
        
        return {
            'overall_intent': overall_intent,
            'segment_intents': segment_intents,
            'total_segments': len(segment_intents)
        }
    
    def get_intent_recommendations(self, intent_type):
        """
        Рекомендации в зависимости от намерения
        
        Returns:
            list: рекомендации для оператора
        """
        recommendations = {
            "жалоба": [
                "Извинитесь за неудобства",
                "Выслушайте все претензии полностью",
                "Предложите решение (замена, возврат, компенсация)",
                "Зафиксируйте детали для отдела контроля качества",
                "Предложите обратную связь после решения проблемы"
            ],
            "консультация": [
                "Внимательно выслушайте вопрос",
                "Дайте полный и точный ответ",
                "Предложите дополнительную информацию",
                "Уточните, все ли понятно клиенту",
                "Предложите помощь в будущем"
            ],
            "заказ": [
                "Уточните детали заказа",
                "Предложите сопутствующие товары",
                "Объясните условия доставки и оплаты",
                "Подтвердите контактные данные",
                "Поблагодарите за заказ"
            ],
            "поддержка": [
                "Попросите описать проблему подробно",
                "Предложите пошаговое решение",
                "Если не можете решить - передайте специалисту",
                "Зафиксируйте обращение в системе",
                "Уточните, решена ли проблема"
            ],
            "отмена": [
                "Выясните причину отмены",
                "Предложите альтернативы",
                "Объясните условия возврата",
                "Извинитесь, даже если причина не в компании",
                "Сохраните лояльность клиента"
            ],
            "статус": [
                "Быстро найдите информацию по заказу",
                "Объясните текущий статус простыми словами",
                "Если есть задержка - извинитесь и объясните причину",
                "Предложите отслеживание в реальном времени",
                "Уточните, нужна ли дополнительная помощь"
            ],
            "сотрудничество": [
                "Перенаправьте на отдел продаж/партнерств",
                "Соберите контактные данные",
                "Зафиксируйте интерес в CRM",
                "Предложите отправить коммерческое предложение",
                "Договоритесь о дальнейшем общении"
            ],
            "неопределено": [
                "Внимательно выслушайте клиента",
                "Задавайте уточняющие вопросы",
                "Определите реальную потребность",
                "Перенаправьте при необходимости",
                "Предложите помощь в любом случае"
            ]
        }
        
        return recommendations.get(intent_type, [
            "Проявите эмпатию и внимательность",
            "Задавайте уточняющие вопросы",
            "Предлагайте конкретные решения",
            "Следите за тоном голоса",
            "Завершите разговор на позитивной ноте"
        ])


class MLIntentDetector(IntentDetector):
    """
    Детектор намерений с ML-компонентами
    """
    
    def __init__(self, use_ml=True):
        super().__init__()
        self.use_ml = use_ml
        
        if use_ml:
            try:
                from transformers import pipeline
                # Можно использовать модель для классификации текста
                self.classifier = pipeline(
                    "zero-shot-classification",
                    model="cointegrated/rubert-tiny2-cedr-emotion-detection"
                )
                self.ml_available = True
            except:
                print("ML модель не загружена, используется rule-based")
                self.ml_available = False
        else:
            self.ml_available = False
    
    def detect_intent_ml(self, text):
        """
        Определение намерений с помощью ML
        """
        if not self.ml_available or not text.strip():
            return self.detect_intent_combined(text)
        
        # Кандидаты намерений
        candidate_intents = list(self.intent_patterns.keys())
        
        try:
            result = self.classifier(
                text,
                candidate_labels=candidate_intents,
                multi_label=False
            )
            
            return {
                "main_intent": result['labels'][0],
                "main_intent_score": round(result['scores'][0], 3),
                "confidence": "высокая" if result['scores'][0] > 0.7 else "средняя",
                "all_intents": dict(zip(result['labels'], result['scores'])),
                "method": "ml"
            }
        except Exception as e:
            print(f"ML детектирование не удалось: {e}")
            return self.detect_intent_combined(text)


if __name__ == "__main__":
    # Тестирование детектора намерений
    detector = IntentDetector()
    
    test_texts = [
        "У меня сломался телефон, купленный у вас неделю назад. Хочу вернуть деньги!",
        "Подскажите, пожалуйста, как пользоваться этой функцией в приложении?",
        "Здравствуйте, хочу заказать у вас ноутбук с доставкой на дом.",
        "Не могу войти в личный кабинет, что делать?",
        "Передумал покупать, хочу отменить заказ номер 12345."
    ]
    
    print("Тест определения намерений:")
    print("-" * 50)
    
    for i, text in enumerate(test_texts):
        result = detector.detect_intent_combined(text)
        print(f"Текст {i+1}: {text[:60]}...")
        print(f"Основное намерение: {result['main_intent']}")
        print(f"Уверенность: {result['confidence']}")
        
        # Показываем топ-3 намерения
        sorted_intents = sorted(
            result['all_intents'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        print("Топ-3 намерения:")
        for intent, score in sorted_intents:
            print(f"  - {intent}: {score}")
        
        print("-" * 50)