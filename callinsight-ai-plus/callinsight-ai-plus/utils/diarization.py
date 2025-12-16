# diarization.py (упрощенная версия)
import os  # ⬅️ ДОБАВИТЬ ЭТУ СТРОКУ!
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class SimpleDiarizer:
    """
    Упрощенный диаризатор для демо
    """
    
    def __init__(self, n_speakers=2):
        self.n_speakers = n_speakers
    
    def diarize(self, audio_path):
        """
        Демо-версия диаризации
        """
        # Проверяем существует ли файл
        if not os.path.exists(audio_path):
            return {
                'success': False,
                'error': f'Файл не найден: {audio_path}',
                'segments': [],
                'speaker_stats': {}
            }
        
        # Возвращаем демо-данные
        segments = [
            {
                'speaker': 'speaker_1',
                'start': 0.0,
                'end': 30.5,
                'duration': 30.5,
                'text': 'Здравствуйте, это служба поддержки. Чем могу помочь?'
            },
            {
                'speaker': 'speaker_2',
                'start': 30.5,
                'end': 90.2,
                'duration': 59.7,
                'text': 'Здравствуйте. У меня проблема с доставкой заказа номер A-12345. Он должен был прийти вчера.'
            },
            {
                'speaker': 'speaker_1',
                'start': 90.2,
                'end': 150.8,
                'duration': 60.6,
                'text': 'Понимаю ваше беспокойство. Давайте проверим статус вашего заказа...'
            }
        ]
        
        speaker_stats = {
            'speaker_1': {
                'total_duration': 91.1,
                'segment_count': 2,
                'avg_duration': 45.55
            },
            'speaker_2': {
                'total_duration': 59.7,
                'segment_count': 1,
                'avg_duration': 59.7
            }
        }
        
        return {
            'success': True,
            'segments': segments,
            'speaker_count': self.n_speakers,
            'speaker_stats': speaker_stats,
            'total_duration': 150.8
        }

class SpeakerDiarizer(SimpleDiarizer):
    """Алиас для совместимости"""
    pass

if __name__ == "__main__":
    diarizer = SpeakerDiarizer(n_speakers=2)
    print("Диаризатор инициализирован (демо-версия)")
    
    # Тестирование
    test_audio = "audio_samples/dialogue.wav"
    if os.path.exists(test_audio):
        result = diarizer.diarize(test_audio)
        print(f"Результат: {result['success']}")
    else:
        print(f"Тестовый файл не найден: {test_audio}")