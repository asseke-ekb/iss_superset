# Apache Superset - Production Build (Russian)

## Что сделано

### 1. Docker образ с русской локализацией

Создан production-ready Docker образ Apache Superset с:

- **Только русский язык** - удалены все остальные переводы для уменьшения размера образа
- **Базовые образы из Harbor** - используются `harbor.fms.kz/library/node:20-trixie-slim` и `harbor.fms.kz/library/python:3.11.13-slim-trixie`
- **ClickHouse драйвер** - установлен `clickhouse-connect` для подключения к ClickHouse базам данных
- **Кастомный логотип** - `custom_logo.png` заменяет стандартный логотип Superset

### 2. Кастомная CSS стилизация

В `superset_config.py` добавлены стили:

- Шрифт Montserrat
- Градиентные заголовки
- Стилизованные KPI карточки
- Улучшенные фильтры и навигация
- Адаптивный дизайн

### 3. Конфигурация

- PostgreSQL 16 как метадата база
- Redis 7 для кэширования и Celery
- Celery worker и beat для фоновых задач
- Gunicorn для production-режима

## Структура файлов

```
docker-prod/
├── Dockerfile.prod          # Multi-stage Dockerfile
├── docker-compose.prod.yml  # Docker Compose конфигурация
├── custom_logo.png          # Кастомный логотип
├── pythonpath_prod/
│   └── superset_config.py   # Конфигурация Superset
└── README.md                # Этот файл
```

## Локальная сборка и запуск

### Сборка образа

```bash
cd superset
docker build -f docker-prod/Dockerfile.prod -t superset-ru:latest .
```

### Создание .env.prod файла

```bash
cp .env.prod.example .env.prod
# Отредактируйте .env.prod и установите:
# - SUPERSET_SECRET_KEY (обязательно! используйте openssl rand -base64 42)
# - POSTGRES_PASSWORD
# - Другие переменные по необходимости
```

### Запуск

```bash
docker compose -f docker-prod/docker-compose.prod.yml up -d
```

### Доступ

- URL: http://localhost:8088
- Логин по умолчанию: admin / admin

## Что нужно сделать (DevOps)

### 1. Пуш образа в Harbor

```bash
# Тегирование образа для Harbor
docker tag superset-ru:latest harbor.fms.kz/library/superset:latest
docker tag superset-ru:latest harbor.fms.kz/library/superset:v1.0.0

# Авторизация в Harbor
docker login harbor.fms.kz

# Пуш образа
docker push harbor.fms.kz/library/superset:latest
docker push harbor.fms.kz/library/superset:v1.0.0
```

### 2. Обновление docker-compose для production

После пуша в Harbor, измените `docker-compose.prod.yml`:

```yaml
x-superset-common: &superset-common
  image: harbor.fms.kz/library/superset:latest  # Изменить на Harbor образ
  pull_policy: always                            # Изменить на always
```

### 3. Настройка production окружения

1. **Секреты** - установите уникальный `SUPERSET_SECRET_KEY`
2. **База данных** - настройте внешний PostgreSQL (опционально)
3. **Redis** - настройте внешний Redis кластер (опционально)
4. **SSL/TLS** - настройте reverse proxy (nginx/traefik) с SSL
5. **Мониторинг** - добавьте health checks и алерты

### 4. CI/CD (опционально)

Рекомендуется настроить автоматическую сборку при изменениях:

```yaml
# Пример GitLab CI
build:
  stage: build
  script:
    - docker build -f docker-prod/Dockerfile.prod -t harbor.fms.kz/library/superset:$CI_COMMIT_SHA .
    - docker push harbor.fms.kz/library/superset:$CI_COMMIT_SHA
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SUPERSET_SECRET_KEY` | Секретный ключ (обязательно!) | - |
| `SUPERSET_PORT` | Порт Superset | 8088 |
| `POSTGRES_USER` | Пользователь PostgreSQL | superset |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | superset |
| `POSTGRES_DB` | Имя базы данных | superset |

## Полезные команды

```bash
# Просмотр логов
docker compose -f docker-prod/docker-compose.prod.yml logs -f superset

# Перезапуск
docker compose -f docker-prod/docker-compose.prod.yml restart superset

# Остановка
docker compose -f docker-prod/docker-compose.prod.yml down

# Полная очистка (включая volumes)
docker compose -f docker-prod/docker-compose.prod.yml down -v
```

## Примечания

- Образ содержит только русский язык (`ru`) - английский и другие языки удалены
- При первом запуске `superset-init` создает администратора и инициализирует базу
- Celery worker необходим для выполнения асинхронных задач (отчеты, алерты)
- Celery beat необходим для планировщика задач
