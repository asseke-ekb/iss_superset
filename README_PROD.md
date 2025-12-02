# 🚀 Superset Production - Готовый к развертыванию

## 📦 Что включено

✅ **Apache Superset 4.1.1** - Production версия
✅ **Кастомный логотип** - 80px в навбаре
✅ **Русский + Английский** языки
✅ **Карта Kazakhstan** - для Country Map визуализации
✅ **CSV/Excel upload** - загрузка файлов
✅ **ClickHouse поддержка** - драйвер clickhouse-connect
✅ **Production оптимизация** - минифицированный код

---

## ⚡ Быстрый старт (2 команды!)

```bash
cd docker-prod
./deploy.sh
```

**Готово!** Откройте http://localhost:8088

---

## 📋 Что нужно DevOps

### Вариант 1: Docker Compose (рекомендуется)
```bash
cd docker-prod
docker build -f Dockerfile.prod -t superset-prod:latest ..
docker compose -f docker-compose.prod.yml up -d
```

### Вариант 2: Kubernetes
```bash
# 1. Собрать образ
docker build -f docker-prod/Dockerfile.prod -t superset-prod:latest .

# 2. Загрузить в registry
docker tag superset-prod:latest YOUR_REGISTRY/superset-prod:4.1.1
docker push YOUR_REGISTRY/superset-prod:4.1.1

# 3. Обновить docker-prod/k8s/*.yaml (заменить YOUR_REGISTRY)

# 4. Развернуть
kubectl create namespace superset
kubectl apply -f docker-prod/k8s/ -n superset
```

---

## 📁 Структура проекта

```
iss_superset/
├── docker-prod/                    # 🎯 ВСЁ ДЛЯ PRODUCTION
│   ├── Dockerfile.prod            # Production Dockerfile
│   ├── docker-compose.prod.yml    # Docker Compose конфигурация
│   ├── deploy.sh                  # Скрипт быстрого развертывания
│   ├── custom_logo.png            # Логотип
│   ├── pythonpath_prod/           # Production конфигурация
│   ├── k8s/                       # Kubernetes манифесты
│   ├── DEPLOY.md                  # Подробная инструкция
│   └── README_KUBERNETES.md       # Инструкция для K8s
├── superset/                       # Backend код
│   └── translations/              # Переводы (ru, en)
├── superset-frontend/             # Frontend код
│   └── plugins/legacy-plugin-chart-country-map/
│       └── src/countries/
│           └── kazakhstan.geojson # Карта Kazakhstan
└── README_PROD.md                 # 👈 Этот файл
```

---

## 🔐 Первый вход

- **URL:** http://localhost:8088
- **Логин:** `admin`
- **Пароль:** `admin`

⚠️ **ВАЖНО:** Смените пароль после первого входа!

---

## ⚙️ Переменные окружения

Скопируйте пример и настройте:
```bash
cd docker-prod
cp .env.prod.example .env.prod
```

Обязательно измените в `.env.prod`:
- `SUPERSET_SECRET_KEY` - сгенерируйте: `openssl rand -base64 42`
- `DATABASE_PASSWORD` - надежный пароль для БД
- `POSTGRES_PASSWORD` - тот же пароль для PostgreSQL

---

## 🐳 Docker команды

```bash
# Логи
docker compose -f docker-prod/docker-compose.prod.yml logs -f superset_app

# Остановка
docker compose -f docker-prod/docker-compose.prod.yml down

# Перезапуск
docker compose -f docker-prod/docker-compose.prod.yml restart superset_app

# Статус
docker compose -f docker-prod/docker-compose.prod.yml ps
```

---

## 📊 Требования

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM минимум
- 10GB диска

---

## 🗄️ Подключение ClickHouse

Superset включает драйвер **clickhouse-connect** для работы с ClickHouse.

### Добавление базы данных ClickHouse:

1. Войдите в Superset
2. Перейдите в **Data → Databases → + Database**
3. Выберите **"ClickHouse Connect"** из списка
4. Введите параметры подключения:
   - **Host:** имя хоста или IP (например, `clickhouse-server`)
   - **Port:** `8123` (HTTP) или `8443` (HTTPS)
   - **Database name:** `default` (или имя вашей БД)
   - **Username:** `default`
   - **Password:** (если требуется)

### Формат URI подключения:

```
clickhousedb://username:password@host:port/database
```

**Примеры:**
- HTTP: `clickhousedb://default:@clickhouse-server:8123/default`
- HTTPS: `clickhousedb://user:pass@clickhouse:8443/mydb?protocol=https`

**Дополнительные параметры:**
- `secure=true` - использовать HTTPS
- `verify=false` - отключить проверку SSL
- `compress=true` - включить сжатие

Подробная документация в файле: [docker-prod/pythonpath_prod/superset_config.py](docker-prod/pythonpath_prod/superset_config.py#L171)

---

## 📖 Дополнительная информация

- [Подробная инструкция](docker-prod/DEPLOY.md)
- [Kubernetes](docker-prod/README_KUBERNETES.md)
- [ClickHouse подключение](docker-prod/CLICKHOUSE.md)
- [Список файлов для DevOps](ПЕРЕДАТЬ_DEVOPS.txt)

---

## ❓ Проблемы?

1. **Порт 8088 занят:** Измените порт в `docker-compose.prod.yml`
2. **Ошибка сборки:** Очистите Docker cache: `docker builder prune -af`
3. **Логи:** `docker compose -f docker-prod/docker-compose.prod.yml logs -f`

---

**Готово к передаче DevOps!** 🎉
