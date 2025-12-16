# profanity.py - Улучшенная версия с примером словаря
import re

class ProfanityFilter:
    def __init__(self, dictionary_path=None):
        # Базовый словарь нецензурных слов (можно расширить)
        self.profanity_words = [
            "плохоеслово1",  # Замените на реальные слова
            "оскорбление",
            # Добавьте сюда свой список
        ]
        
        # Загрузка кастомного словаря
        if dictionary_path:
            try:
                with open(dictionary_path, 'r', encoding='utf-8') as f:
                    custom_words = [line.strip() for line in f if line.strip()]
                    self.profanity_words.extend(custom_words)
            except FileNotFoundError:
                print(f"Файл словаря {dictionary_path} не найден, используется базовый список.")
        
        # Создаем регулярные выражения для поиска
        self.patterns = []
        for word in self.profanity_words:
            # Учитываем возможные морфологические варианты
            pattern = re.compile(r'\b' + re.escape(word) + r'\w*\b', re.IGNORECASE)
            self.patterns.append(pattern)
    
    def contains_profanity(self, text):
        matches = []
        for pattern in self.patterns:
            found = pattern.findall(text)
            if found:
                matches.extend(found)
        return len(matches) > 0, matches
    
    def mask_profanity(self, text):
        masked_text = text
        for pattern in self.patterns:
            # Заменяем каждое найденное слово на звездочки
            def replace_func(match):
                return '*' * len(match.group())
            masked_text = pattern.sub(replace_func, masked_text)
        return masked_text
    
    def analyze_conversation(self, dialog):
        stats = {
            "total_profanity_count": 0,
            "profanity_by_speaker": {"operator": 0, "client": 0},
            "masked_dialog": []
        }
        
        for line in dialog:
            has_profanity, words = self.contains_profanity(line["text"])
            
            if has_profanity:
                stats["total_profanity_count"] += len(words)
                speaker = line.get("speaker", "client")
                if speaker in stats["profanity_by_speaker"]:
                    stats["profanity_by_speaker"][speaker] += len(words)
                else:
                    stats["profanity_by_speaker"][speaker] = len(words)
                
                stats["masked_dialog"].append({
                    **line,
                    "text": self.mask_profanity(line["text"]),
                    "profanity_found": True,
                    "profanity_words": words
                })
            else:
                stats["masked_dialog"].append({
                    **line,
                    "text": line["text"],
                    "profanity_found": False,
                    "profanity_words": []
                })
        
        return stats