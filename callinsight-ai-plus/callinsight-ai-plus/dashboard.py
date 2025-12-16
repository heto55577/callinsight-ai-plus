# dashboard.py
import json
from io import BytesIO
import base64

class CallInsightDashboard:
    """Простой генератор дашбордов"""
    
    def __init__(self):
        self.color_map = {
            'радость': '#2ecc71',
            'гнев': '#e74c3c',
            'страх': '#9b59b6',
            'грусть': '#3498db',
            'удивление': '#e67e22',
            'нейтрально': '#95a5a6'
        }
    
    def create_emotion_chart_html(self, emotion_stats):
        """Создание HTML для графика эмоций"""
        if not emotion_stats:
            return "<div class='alert alert-info'>Нет данных об эмоциях</div>"
        
        html = """
        <div class="dashboard-card">
            <h5>😊 Распределение эмоций</h5>
            <div class="row">
        """
        
        for emotion, value in emotion_stats.items():
            color = self.color_map.get(emotion, '#95a5a6')
            html += f"""
                <div class="col-md-4 mb-3">
                    <div class="metric-card">
                        <div class="metric-value" style="color: {color}">{value}%</div>
                        <div class="metric-label">{emotion}</div>
                    </div>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def create_keywords_html(self, keywords):
        """Создание HTML для ключевых слов"""
        if not keywords:
            return "<div class='alert alert-info'>Нет ключевых слов</div>"
        
        html = """
        <div class="dashboard-card">
            <h5>🔑 Ключевые слова</h5>
            <div class="keyword-cloud">
        """
        
        for keyword in keywords[:10]:  # Берем только топ-10
            html += f'<span class="badge bg-info text-dark m-1 p-2">{keyword}</span>'
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def create_metrics_table(self, call_data):
        """Создание таблицы с метриками"""
        html = """
        <div class="dashboard-card">
            <h5>📊 Статистика звонка</h5>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Метрика</th>
                        <th>Значение</th>
                        <th>Статус</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        metrics = [
            ("Длительность", call_data.get('duration', 'N/A'), "нормально"),
            ("Доминирующая эмоция", call_data.get('dominant_emotion', 'неизвестно'), 
             "критично" if call_data.get('dominant_emotion') == 'гнев' else "нормально"),
            ("Нецензурная лексика", f"{call_data.get('total_profanity_count', 0)} случаев", 
             "высокий" if call_data.get('total_profanity_count', 0) > 3 else "низкий"),
            ("Тональность", f"{call_data.get('sentiment_score', 0.5)*100:.1f}% позитива", 
             "высокая" if call_data.get('sentiment_score', 0.5) > 0.7 else "низкая"),
            ("Ключевых тем", len(call_data.get('keywords', [])), 
             "много" if len(call_data.get('keywords', [])) > 5 else "мало")
        ]
        
        for metric, value, status in metrics:
            status_class = {
                "критично": "danger",
                "высокий": "warning",
                "низкий": "success",
                "высокая": "success",
                "низкая": "warning",
                "нормально": "info",
                "много": "info",
                "мало": "secondary"
            }.get(status, "secondary")
            
            html += f"""
                <tr>
                    <td>{metric}</td>
                    <td><strong>{value}</strong></td>
                    <td><span class="badge bg-{status_class}">{status}</span></td>
                </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return html
    
    def create_recommendations(self, call_data):
        """Создание рекомендаций на основе анализа"""
        recommendations = []
        
        # Анализ эмоций
        dominant_emotion = call_data.get('dominant_emotion', 'нейтрально')
        if dominant_emotion == 'гнев':
            recommendations.append("🚨 Клиент раздражен. Рекомендуется срочный обратный звонок.")
        elif dominant_emotion == 'грусть':
            recommendations.append("😢 Клиент расстроен. Предложите дополнительную помощь или компенсацию.")
        
        # Анализ нецензурной лексики
        profanity_count = call_data.get('total_profanity_count', 0)
        if profanity_count > 3:
            recommendations.append("⚠️ Высокий уровень агрессии. Рассмотрите эскалацию к менеджеру.")
        elif profanity_count > 0:
            recommendations.append("📝 Зафиксируйте случаи нецензурной лексики для обучения операторов.")
        
        # Анализ тональности
        sentiment_score = call_data.get('sentiment_score', 0.5)
        if sentiment_score < 0.3:
            recommendations.append("📉 Отрицательная тональность. Требуется дополнительное обучение оператора.")
        
        if not recommendations:
            recommendations.append("✅ Звонок прошел в нормальном тоне. Продолжайте в том же духе!")
        
        html = """
        <div class="dashboard-card">
            <h5>💡 Рекомендации</h5>
            <ul class="recommendations-list">
        """
        
        for rec in recommendations:
            html += f'<li>{rec}</li>'
        
        html += """
            </ul>
        </div>
        """
        
        return html
    
    def create_complete_dashboard(self, call_data):
        """Создание полного дашборда"""
        dashboard_html = f"""
        <div class="dashboard-container">
            <div class="row mb-4">
                <div class="col-md-12">
                    {self.create_emotion_chart_html(call_data.get('emotion_stats', {}))}
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    {self.create_keywords_html(call_data.get('keywords', []))}
                </div>
                
                <div class="col-md-6">
                    {self.create_metrics_table(call_data)}
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-12">
                    {self.create_recommendations(call_data)}
                </div>
            </div>
        </div>
        """
        
        return dashboard_html

if __name__ == "__main__":
    dashboard = CallInsightDashboard()
    
    # Тестовые данные
    test_data = {
        'call_id': 1,
        'duration': '05:23',
        'emotion_stats': {'радость': 15, 'гнев': 25, 'нейтрально': 45, 'грусть': 10, 'удивление': 5},
        'keywords': ['доставка', 'качество', 'проблема', 'возврат', 'деньги'],
        'total_profanity_count': 2,
        'dominant_emotion': 'гнев',
        'sentiment_score': 0.3
    }
    
    html = dashboard.create_complete_dashboard(test_data)
    print("Дашборд сгенерирован успешно!")