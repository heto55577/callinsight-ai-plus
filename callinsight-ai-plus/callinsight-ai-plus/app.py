# app.py
from flask import Flask, render_template, request, jsonify
import os

# Пытаемся импортировать dashboard
try:
    from dashboard import CallInsightDashboard
    dashboard_generator = CallInsightDashboard()
    print("✅ Dashboard module loaded successfully")
except ImportError as e:
    print(f"⚠️ Dashboard module not found: {e}")
    # Создаем простой дашборд
    class SimpleDashboard:
        def create_complete_dashboard(self, call_data):
            return f"""
            <div class="dashboard-container">
                <div class="alert alert-info">
                    <h4>📊 Демо-дашборд для звонка #{call_data.get('call_id', 'N/A')}</h4>
                    <p>Основные компоненты: эмоции, ключевые слова, статистика</p>
                </div>
            </div>
            """
    dashboard_generator = SimpleDashboard()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Создаем папки если их нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    """Главная страница со списком звонков"""
    calls = [
        {"id": 1, "duration": "05:23", "date": "2024-03-15", "score": 75},
        {"id": 2, "duration": "03:45", "date": "2024-03-14", "score": 90},
        {"id": 3, "duration": "07:12", "date": "2024-03-13", "score": 60},
    ]
    return render_template('index.html', calls=calls)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """Анализ загруженного аудио"""
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Сохраняем файл
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Возвращаем демо-данные
    analysis_results = {
        'call_id': len(os.listdir(app.config['UPLOAD_FOLDER'])),
        'filename': file.filename,
        'dominant_emotion': 'гнев',
        'emotion_score': 0.8,
        'keywords': ['проблема', 'доставка', 'жалоба', 'качество', 'возврат'],
        'has_profanity': True,
        'total_profanity_count': 2,
        'profanity_stats': {'клиент': 2, 'оператор': 0},
        'sentiment_score': 0.3,
        'transcript': 'Демо-текст: клиент жалуется на задержку доставки...'
    }
    
    return jsonify(analysis_results)

@app.route('/dashboard/<int:call_id>')
def show_dashboard(call_id):
    """Отображение дашборда для конкретного звонка"""
    
    # Маппинг эмоций для CSS классов
    emotion_class_map = {
        'гнев': 'anger',
        'радость': 'joy', 
        'грусть': 'sadness',
        'страх': 'fear',
        'удивление': 'surprise',
        'нейтрально': 'neutral'
    }
    
    dominant_emotion = 'гнев'
    emotion_class = emotion_class_map.get(dominant_emotion, 'neutral')
    
    call_data = {
        'call_id': call_id,
        'duration': '05:23',
        'date': '2024-03-15',
        'emotion_stats': {
            'радость': 15,
            'нейтрально': 45,
            'гнев': 25,
            'грусть': 10,
            'удивление': 5
        },
        'keywords': ['доставка', 'качество', 'проблема', 'возврат', 'деньги', 
                    'сервис', 'жалоба', 'решение', 'срок', 'товар'],
        'sentiment_score': 0.65,
        'total_profanity_count': 2,
        'dominant_emotion': dominant_emotion,
        'dominant_emotion_class': emotion_class,
        'metrics': {
            'Длительность': {'value': '05:23', 'status': 'нормально'},
            'Эмоциональный индекс': {'value': '65/100', 'status': 'хорошо'},
            'Уровень агрессии': {'value': 'Средний', 'status': 'нормально'},
            'Ключевых тем': {'value': '8', 'status': 'хорошо'},
            'Рекомендации': {'value': '3', 'status': 'нормально'}
        }
    }
    
    # Генерируем дашборд
    dashboard_html = dashboard_generator.create_complete_dashboard(call_data)
    
    return render_template('dashboard.html', 
                         dashboard_html=dashboard_html,
                         call_data=call_data)

if __name__ == '__main__':
    print("🚀 Starting CallInsight AI+...")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)