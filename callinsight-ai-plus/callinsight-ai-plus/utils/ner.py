# ner.py (упрощенная версия без spacy)
import re
from datetime import datetime
from typing import List, Dict, Any

class NamedEntityRecognizer:
    """
    Извлечение именованных сущностей из текста (regex-based)
    """
    
    def __init__(self):
        # Регулярные выражения для извлечения сущностей
        self.patterns = {
            'phone': [
                r'\+7\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}',
                r'8\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
            ],
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ],
            'date': [
                r'\d{1,2}[\s./-]\d{1,2}[\s./-]\d{2,4}',  # DD.MM.YYYY
                r'\d{4}[\s./-]\d{1,2}[\s./-]\d{1,2}'     # YYYY-MM-DD
            ],
            'money': [
                r'\d+[\s,]?\d*[\s,]?\d*\s*(?:руб|р|RUB)',
                r'(?:руб|р|RUB)\s*\d+[\s,]?\d*[\s,]?\d*'
            ],
            'order_number': [
                r'(?:заказ|номер|order|#)\s*(?:№|#)?\s*[A-Za-z0-9-]+',
                r'[A-Z]-?\d{5,}'
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Основной метод извлечения сущностей
        """
        entities = {category: [] for category in self.patterns.keys()}
        
        for category, patterns in self.patterns.items():
            found_entities = []
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    
                    match = match.strip()
                    if match and match not in found_entities:
                        found_entities.append(match)
            
            entities[category] = found_entities
        
        # Обработка результатов
        processed_entities = {}
        
        for category, items in entities.items():
            if items:
                processed_entities[category] = {
                    'count': len(items),
                    'values': items,
                    'unique': list(set(items))
                }
        
        return {
            'entities': processed_entities,
            'total_entities': sum(len(v) for v in entities.values()),
            'unique_categories': len([v for v in processed_entities.values() if v['values']])
        }
    
    def extract_from_text(self, text: str) -> Dict[str, List[str]]:
        """Простой интерфейс для извлечения сущностей"""
        result = self.extract_entities(text)
        
        # Форматируем в простой вид
        simple_result = {}
        for category, data in result['entities'].items():
            simple_result[category] = data['values']
        
        return simple_result

if __name__ == "__main__":
    ner = NamedEntityRecognizer()
    
    test_text = """
    Мой заказ номер A-12345 должен быть доставлен 15.03.2024.
    Сумма заказа 85 000 руб. Мой телефон +7 (999) 123-45-67.
    Email: client@example.com.
    """
    
    print("Тест NER (упрощенная версия):")
    result = ner.extract_from_text(test_text)
    
    for category, items in result.items():
        if items:
            print(f"{category}: {items}")