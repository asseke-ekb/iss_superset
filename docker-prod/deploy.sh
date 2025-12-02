#!/bin/bash
set -e

echo "=================================="
echo "Superset Production Deployment"
echo "=================================="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker не установлен!"
    exit 1
fi

# Проверка Docker Compose
if ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose не установлен!"
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"
echo ""

# Проверка .env.prod
if [ ! -f ".env.prod" ]; then
    echo "⚠️  Файл .env.prod не найден!"
    echo "Создаю из .env.prod.example..."
    if [ -f ".env.prod.example" ]; then
        cp .env.prod.example .env.prod
        echo "✅ Файл .env.prod создан"
        echo ""
        echo "⚠️  ВАЖНО: Откройте .env.prod и измените:"
        echo "   - SUPERSET_SECRET_KEY"
        echo "   - DATABASE_PASSWORD"
        echo "   - POSTGRES_PASSWORD"
        echo ""
        read -p "Нажмите Enter когда настроите .env.prod..."
    else
        echo "❌ .env.prod.example не найден!"
        exit 1
    fi
fi

# Шаг 1: Сборка образа
echo "📦 Шаг 1/3: Сборка production образа..."
echo "Это займёт 20-40 минут. Можете пойти попить кофе ☕"
docker build -f Dockerfile.prod -t superset-prod:latest .. || {
    echo "❌ Ошибка сборки!"
    exit 1
}
echo "✅ Образ собран успешно!"
echo ""

# Шаг 2: Остановка старых контейнеров (если есть)
echo "🔄 Шаг 2/3: Остановка старых контейнеров..."
docker compose -f docker-compose.prod.yml down 2>/dev/null || true
echo "✅ Готово"
echo ""

# Шаг 3: Запуск
echo "🚀 Шаг 3/3: Запуск Superset..."
docker compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Ожидание запуска контейнеров (60 сек)..."
sleep 60

# Проверка статуса
echo ""
echo "📊 Статус контейнеров:"
docker compose -f docker-compose.prod.yml ps

echo ""
echo "=================================="
echo "✅ Развертывание завершено!"
echo "=================================="
echo ""
echo "🌐 Superset доступен по адресу:"
echo "   http://localhost:8088"
echo ""
echo "👤 Данные для входа:"
echo "   Логин:  admin"
echo "   Пароль: admin"
echo ""
echo "⚠️  ВАЖНО: Смените пароль после первого входа!"
echo ""
echo "📝 Просмотр логов:"
echo "   docker compose -f docker-compose.prod.yml logs -f superset_app"
echo ""
echo "🛑 Остановка:"
echo "   docker compose -f docker-compose.prod.yml down"
echo ""
