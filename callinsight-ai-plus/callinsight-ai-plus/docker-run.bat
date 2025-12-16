@echo off
echo ============================================
echo    CallInsight AI+ - Docker Launcher
echo ============================================
echo.

:: Проверка Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен!
    echo.
    echo Установите Docker Desktop:
    echo 📥 https://www.docker.com/products/docker-desktop/
    echo.
    echo После установки перезагрузите компьютер.
    pause
    exit /b 1
)

echo 1. Собираю Docker образ...
docker build -t callinsight-ai .

echo.
echo 2. Запускаю контейнер...
echo    Приложение будет доступно по адресу: http://localhost:5000
echo.
docker run -d --name callinsight-app -p 5000:5000 callinsight-ai

echo.
echo ✅ Контейнер запущен!
echo.
echo Команды для управления:
echo    📊 Просмотр логов:   docker logs callinsight-app
echo    ⏹️ Остановить:       docker stop callinsight-app
echo    ▶️ Запустить:        docker start callinsight-app
echo    🔄 Перезапустить:    docker restart callinsight-app
echo    ❌ Удалить:          docker rm -f callinsight-app
echo.
echo 🌐 Откройте: http://localhost:5000
echo.
pause