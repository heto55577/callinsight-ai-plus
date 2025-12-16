# transcribe.py (упрощенная версия)
import os  # ⬅️ УЖЕ ЕСТЬ, но проверьте что он в начале файла
import wave
import tempfile

class AudioTranscriber:
    def __init__(self, language="ru-RU"):
        self.language = language
    
    def get_audio_info(self, audio_path):
        """Получение информации об аудиофайле"""
        try:
            # Проверяем существует ли файл
            if not os.path.exists(audio_path):
                return {
                    "error": f"Файл не найден: {audio_path}",
                    "duration_seconds": 0,
                    "duration_formatted": "00:00"
                }
            
            # Используем wave для анализа
            with wave.open(audio_path, 'rb') as wf:
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                frames = wf.getnframes()
                duration = frames / float(framerate)
            
            return {
                "duration_seconds": round(duration, 2),
                "duration_formatted": self._format_time(duration),
                "sample_rate": framerate,
                "channels": channels,
                "frames": frames,
                "file_size_mb": round(os.path.getsize(audio_path) / (1024 * 1024), 2),
                "file_exists": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "duration_seconds": 0,
                "duration_formatted": "00:00",
                "file_exists": False
            }
    
    def transcribe(self, audio_path, method="demo"):
        """
        Демо-версия транскрибации
        """
        # Проверяем существует ли файл
        if not os.path.exists(audio_path):
            return {
                "error": f"Файл не найден: {audio_path}",
                "text": "",
                "audio_info": {"error": "File not found"},
                "segments": [],
                "language": self.language,
                "method": method
            }
        
        audio_info = self.get_audio_info(audio_path)
        
        # Демо-текст
        demo_text = """
        Оператор: Здравствуйте, это служба поддержки компании ТехноМаркет. Меня зовут Анна. Чем могу помочь?
        
        Клиент: Здравствуйте. У меня большая проблема с заказом номер A-12345. 
        Я заказал ноутбук ASUS ZenBook неделю назад, оплатил 85 000 рублей, 
        обещали доставку на 15 марта, а сегодня уже 18-е, и ничего не пришло!
        
        Оператор: Понимаю ваше беспокойство. Давайте проверим статус вашего заказа. 
        Вижу, что заказ действительно задерживается из-за проблем на складе поставщика.
        
        Клиент: Это просто ужасно! Мне нужен ноутбук для срочной работы. 
        Что вы можете предложить? Я очень разочарован вашим сервисом.
        
        Оператор: Приношу извинения за неудобства. Я могу предложить два варианта: 
        либо мы ускорим доставку этого заказа с компенсацией 5 000 рублей, 
        либо предложим аналогичную модель со склада с доставкой завтра.
        
        Клиент: Хорошо, давайте второе решение. Но только если будет доставлено точно завтра.
        
        Оператор: Отлично. Я оформляю замену заказа. Новый номер заказа B-67890. 
        Доставка будет завтра с 10 до 14 часов. Отправлю вам подтверждение на email ivanov@example.com.
        
        Клиент: Спасибо. Надеюсь, на этот раз все будет хорошо.
        """
        
        segments = [
            {"start": 0.0, "end": 10.5, "text": "Оператор: Здравствуйте, это служба поддержки компании ТехноМаркет.", "duration": 10.5},
            {"start": 10.5, "end": 35.2, "text": "Клиент: Здравствуйте. У меня большая проблема с заказом номер A-12345.", "duration": 24.7},
            {"start": 35.2, "end": 50.8, "text": "Оператор: Понимаю ваше беспокойство. Давайте проверим статус вашего заказа.", "duration": 15.6},
            {"start": 50.8, "end": 75.3, "text": "Клиент: Это просто ужасно! Мне нужен ноутбук для срочной работы.", "duration": 24.5},
            {"start": 75.3, "end": 95.1, "text": "Оператор: Приношу извинения за неудобства. Я могу предложить два варианта.", "duration": 19.8},
            {"start": 95.1, "end": 105.7, "text": "Клиент: Хорошо, давайте второе решение. Но только если будет доставлено точно завтра.", "duration": 10.6},
            {"start": 105.7, "end": 120.4, "text": "Оператор: Отлично. Я оформляю замену заказа. Новый номер заказа B-67890.", "duration": 14.7},
            {"start": 120.4, "end": 125.0, "text": "Клиент: Спасибо. Надеюсь, на этот раз все будет хорошо.", "duration": 4.6}
        ]
        
        return {
            "text": demo_text,
            "audio_info": audio_info,
            "segments": segments,
            "language": self.language,
            "method": method
        }
    
    def _format_time(self, seconds):
        """Форматирование времени в MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    transcriber = AudioTranscriber(language="ru-RU")
    print("Транскрибатор инициализирован (демо-версия)")
    
    # Тестирование
    test_audio = "audio_samples/test.wav"
    if os.path.exists(test_audio):
        result = transcriber.transcribe(test_audio)
        print(f"Транскрибация успешна. Длительность: {result['audio_info'].get('duration_formatted', 'N/A')}")
    else:
        print(f"Тестовый файл не найден: {test_audio}")
        print("Создайте папку audio_samples и добавьте test.wav для тестирования")