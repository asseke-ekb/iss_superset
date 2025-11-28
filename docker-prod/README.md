# Apache Superset - Production Deployment

Продакшн-сборка Apache Superset с поддержкой только английского (EN) и русского (RU) языков.

## Структура файлов

```
docker-prod/
├── Dockerfile.prod           # Dockerfile для сборки образа
├── docker-compose.prod.yml   # Docker Compose для деплоя
├── .env.prod                 # Переменные окружения (ИЗМЕНИТЬ!)
├── pythonpath_prod/
│   └── superset_config.py    # Конфигурация Superset
├── init-db/                  # Скрипты инициализации БД (опционально)
└── README.md                 # Эта документация
```

## Быстрый старт

### 1. Сборка образа

```bash
# Из корня проекта iss_superset
docker build -f docker-prod/Dockerfile.prod -t superset-prod:latest .
```

### 2. Настройка

**ВАЖНО:** Перед запуском отредактируйте `.env.prod`:

```bash
cd docker-prod
cp .env.prod .env.prod.local  # Сделать локальную копию
```

Измените следующие значения в `.env.prod`:
- `SUPERSET_SECRET_KEY` - сгенерируйте: `openssl rand -base64 42`
- `DATABASE_PASSWORD` - надежный пароль для PostgreSQL
- `POSTGRES_PASSWORD` - тот же пароль

### 3. Запуск

```bash
cd docker-prod
docker compose -f docker-compose.prod.yml up -d
```

### 4. Проверка

```bash
# Статус контейнеров
docker compose -f docker-compose.prod.yml ps

# Логи
docker compose -f docker-compose.prod.yml logs -f superset
```

Superset доступен по адресу: http://localhost:8088

## Учетные данные по умолчанию

- **Логин:** admin
- **Пароль:** admin

**ВАЖНО:** Смените пароль после первого входа!

## Компоненты

| Сервис | Описание | Порт |
|--------|----------|------|
| superset | Веб-приложение (Gunicorn) | 8088 |
| superset-worker | Celery worker для фоновых задач | - |
| superset-worker-beat | Celery beat для планировщика | - |
| db | PostgreSQL 16 | 5432 (внутренний) |
| redis | Redis 7 (кэш и брокер) | 6379 (внутренний) |

## Команды управления

```bash
# Остановить
docker compose -f docker-compose.prod.yml down

# Остановить и удалить данные
docker compose -f docker-compose.prod.yml down -v

# Перезапустить
docker compose -f docker-compose.prod.yml restart

# Пересборка и перезапуск
docker compose -f docker-compose.prod.yml up -d --build

# Создать нового администратора
docker exec -it superset_app superset fab create-admin \
    --username newadmin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password newpassword
```

## Настройка HTTPS (рекомендуется)

Для продакшна рекомендуется использовать reverse proxy (nginx) с SSL:

```nginx
server {
    listen 443 ssl;
    server_name superset.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8088;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Смена языка на русский

1. Войдите в Superset
2. Кликните на иконку профиля (правый верхний угол)
3. Выберите **Settings** → **User Settings**
4. В поле **Language** выберите **Russian**
5. Нажмите **Save**

## Резервное копирование

```bash
# Бэкап базы данных
docker exec superset_db pg_dump -U superset superset > backup_$(date +%Y%m%d).sql

# Восстановление
docker exec -i superset_db psql -U superset superset < backup_20231201.sql
```

## Логирование

Логи доступны через Docker:

```bash
# Все сервисы
docker compose -f docker-compose.prod.yml logs -f

# Только приложение
docker compose -f docker-compose.prod.yml logs -f superset

# Последние 100 строк
docker compose -f docker-compose.prod.yml logs --tail=100 superset
```

## Мониторинг

Проверка здоровья контейнеров:

```bash
docker compose -f docker-compose.prod.yml ps
```

Все сервисы должны иметь статус `healthy` или `running`.

## Troubleshooting

### Контейнер не запускается

```bash
# Проверить логи
docker compose -f docker-compose.prod.yml logs superset-init

# Проверить переменные окружения
docker compose -f docker-compose.prod.yml config
```

### Ошибка подключения к БД

1. Убедитесь, что `DATABASE_PASSWORD` и `POSTGRES_PASSWORD` совпадают
2. Проверьте, что контейнер `db` запущен и healthy

### Перевод не работает

Убедитесь, что в контейнере есть файлы переводов:

```bash
docker exec superset_app ls -la /app/superset/translations/ru/LC_MESSAGES/
```

Должны быть файлы `messages.json` и `messages.mo`.
