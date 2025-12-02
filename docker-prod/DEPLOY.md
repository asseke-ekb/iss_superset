# Инструкция по развертыванию Superset

## Описание
Production версия Apache Superset 4.1.1 с кастомизацией:
- ✅ Кастомный логотип (80px)
- ✅ Русский и английский языки
- ✅ Карта Kazakhstan
- ✅ CSV/Excel upload
- ✅ Production оптимизация

## Быстрый старт (Docker Compose)

### 1. Сборка образа
```bash
cd docker-prod
docker build -f Dockerfile.prod -t superset-prod:latest ..
```

### 2. Запуск
```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3. Доступ
- URL: http://localhost:8088
- Логин: admin
- Пароль: admin

## Развертывание в Kubernetes

### 1. Сборка и публикация образа
```bash
# Сборка
cd docker-prod
docker build -f Dockerfile.prod -t superset-prod:latest ..

# Тегирование для вашего registry
docker tag superset-prod:latest YOUR_REGISTRY/superset-prod:4.1.1

# Загрузка в registry
docker push YOUR_REGISTRY/superset-prod:4.1.1
```

### 2. Обновите манифесты
В файлах `k8s/*.yaml` замените `YOUR_REGISTRY` на ваш registry.

### 3. Разверните в кластере
```bash
kubectl create namespace superset
kubectl apply -f k8s/ -n superset
```

## Важные файлы

### Dockerfile и сборка
- `docker-prod/Dockerfile.prod` - Production Dockerfile
- `docker-prod/docker-compose.prod.yml` - Docker Compose конфигурация
- `docker-prod/custom_logo.png` - Логотип

### Конфигурация
- `docker-prod/pythonpath_prod/superset_config.py` - Production конфигурация
- `docker-prod/.env.prod` - Переменные окружения

### Переводы
- `superset/translations/ru/` - Русский язык
- `superset/translations/en/` - Английский язык

### Карты
- `superset-frontend/plugins/legacy-plugin-chart-country-map/src/countries/kazakhstan.geojson`

## Переменные окружения

```bash
# База данных
DATABASE_USER=superset
DATABASE_PASSWORD=superset
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_DB=superset

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Superset
SUPERSET_SECRET_KEY=CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET
SUPERSET_LOAD_EXAMPLES=no
```

## Порты

- `8088` - Superset UI
- `5432` - PostgreSQL (internal)
- `6379` - Redis (internal)

## Volumes

- `db_home` - База данных PostgreSQL
- `redis` - Redis данные
- `superset_home` - Superset конфигурация и uploads

## Требования

- Docker 20.10+
- Docker Compose 2.0+ (для Docker Compose)
- Kubernetes 1.20+ (для K8s)
- 4GB RAM минимум
- 10GB свободного места на диске

## Безопасность

**ВАЖНО:** После развертывания:
1. Смените пароль admin
2. Измените SUPERSET_SECRET_KEY на случайное значение
3. Настройте HTTPS (если production)
4. Настройте backup базы данных

## Поддержка

Логи можно посмотреть командой:
```bash
# Docker Compose
docker compose -f docker-compose.prod.yml logs -f superset_app

# Kubernetes
kubectl logs -f deployment/superset -n superset
```
