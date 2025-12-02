# ClickHouse Integration

## Что включено

✅ **clickhouse-connect** драйвер установлен
✅ Поддержка HTTP и HTTPS подключений
✅ Сжатие данных
✅ Готов к использованию

---

## Добавление ClickHouse в Superset

### Способ 1: Через UI (рекомендуется)

1. Войдите в Superset (http://localhost:8088)
2. Перейдите в **Data → Databases**
3. Нажмите **+ Database**
4. Выберите **"ClickHouse Connect"** из списка
5. Заполните форму:
   - **Display Name:** `My ClickHouse`
   - **SQLAlchemy URI:** `clickhousedb://default:@clickhouse-host:8123/default`
6. Нажмите **Test Connection**
7. Если тест прошёл успешно, нажмите **Connect**

### Способ 2: Через SQL Lab

1. Перейдите в **SQL Lab → SQL Editor**
2. В выпадающем списке баз данных выберите **+ Add database**
3. Следуйте инструкциям из Способа 1

---

## Формат подключения

### Базовый формат URI:

```
clickhousedb://[username[:password]@]host[:port][/database][?parameters]
```

### Примеры:

**HTTP (по умолчанию, порт 8123):**
```
clickhousedb://default:@clickhouse-server:8123/default
```

**HTTPS (порт 8443):**
```
clickhousedb://default:password@clickhouse-server:8443/default?protocol=https
```

**С дополнительными параметрами:**
```
clickhousedb://user:pass@host:8123/mydb?secure=true&compress=true
```

---

## Параметры подключения

| Параметр | Значение | Описание |
|----------|----------|----------|
| `protocol` | `http`, `https` | Протокол подключения |
| `secure` | `true`, `false` | Использовать HTTPS |
| `verify` | `true`, `false` | Проверять SSL сертификат |
| `compress` | `true`, `false` | Включить сжатие данных |
| `session_id` | string | Идентификатор сессии |
| `database` | string | База данных по умолчанию |
| `connect_timeout` | integer | Таймаут подключения (сек) |
| `send_receive_timeout` | integer | Таймаут чтения/записи (сек) |

---

## Примеры конфигураций

### Локальный ClickHouse (без пароля):

```
clickhousedb://default:@localhost:8123/default
```

### Удалённый ClickHouse (с HTTPS и паролем):

```
clickhousedb://myuser:mypassword@ch-prod.example.com:8443/analytics?protocol=https&compress=true
```

### ClickHouse Cloud:

```
clickhousedb://default:your_password@your-instance.clickhouse.cloud:8443/default?secure=true
```

### С пользовательским таймаутом:

```
clickhousedb://default:@clickhouse:8123/default?connect_timeout=30&send_receive_timeout=300
```

---

## Проверка подключения

### Через Superset UI:

После добавления базы данных, используйте кнопку **"Test Connection"** для проверки.

### Через SQL Lab:

Выполните тестовый запрос:

```sql
SELECT version()
```

Или:

```sql
SELECT * FROM system.tables LIMIT 10
```

---

## Kubernetes: Добавление ClickHouse сервиса

Если вы используете Kubernetes и хотите развернуть ClickHouse вместе с Superset:

### 1. Создайте файл `k8s/clickhouse.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: clickhouse
  namespace: superset
spec:
  ports:
    - name: http
      port: 8123
      targetPort: 8123
    - name: native
      port: 9000
      targetPort: 9000
  selector:
    app: clickhouse
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: clickhouse
  namespace: superset
spec:
  serviceName: clickhouse
  replicas: 1
  selector:
    matchLabels:
      app: clickhouse
  template:
    metadata:
      labels:
        app: clickhouse
    spec:
      containers:
      - name: clickhouse
        image: clickhouse/clickhouse-server:latest
        ports:
        - containerPort: 8123
          name: http
        - containerPort: 9000
          name: native
        volumeMounts:
        - name: clickhouse-data
          mountPath: /var/lib/clickhouse
  volumeClaimTemplates:
  - metadata:
      name: clickhouse-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### 2. Разверните:

```bash
kubectl apply -f k8s/clickhouse.yaml -n superset
```

### 3. В Superset используйте:

```
clickhousedb://default:@clickhouse:8123/default
```

---

## Docker Compose: Добавление ClickHouse

Если вы хотите добавить ClickHouse в `docker-compose.prod.yml`:

```yaml
services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    environment:
      CLICKHOUSE_DB: default
      CLICKHOUSE_USER: default
      CLICKHOUSE_PASSWORD: ""
    networks:
      - superset-network

volumes:
  clickhouse_data:
```

Затем в Superset используйте:

```
clickhousedb://default:@clickhouse:8123/default
```

---

## Troubleshooting

### Ошибка: "Connection refused"

- Проверьте, что ClickHouse запущен и доступен
- Проверьте правильность хоста и порта
- Убедитесь, что firewall не блокирует порт 8123

### Ошибка: "Authentication failed"

- Проверьте правильность username и password
- Убедитесь, что пользователь имеет права доступа к базе данных

### Ошибка: "SSL certificate verify failed"

Добавьте `verify=false` к URI:
```
clickhousedb://user:pass@host:8443/db?protocol=https&verify=false
```

### Медленные запросы:

- Включите сжатие: `compress=true`
- Увеличьте таймауты: `send_receive_timeout=600`
- Оптимизируйте запросы в ClickHouse

---

## Дополнительные ресурсы

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse Python Driver](https://clickhouse.com/docs/en/integrations/python)
- [Superset Documentation](https://superset.apache.org/docs/databases/clickhouse)
- [clickhouse-connect GitHub](https://github.com/ClickHouse/clickhouse-connect)

---

## Поддерживаемые функции

✅ SELECT запросы
✅ JOIN операции
✅ Агрегатные функции
✅ Window функции
✅ Материализованные представления
✅ Distributed таблицы
✅ Array и Map типы данных
✅ Сжатие данных
✅ SSL/TLS подключения

---

**ClickHouse готов к использованию!** 🚀
