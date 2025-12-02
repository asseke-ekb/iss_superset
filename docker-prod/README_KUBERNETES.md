# Развертывание Superset в Kubernetes

## Подготовка Docker образа

### 1. Тегирование образа для вашего registry
```bash
# Замените YOUR_REGISTRY на ваш registry (например, registry.example.com или docker.io/username)
docker tag superset-prod:latest YOUR_REGISTRY/superset-prod:4.1.1
docker tag superset-prod:latest YOUR_REGISTRY/superset-prod:latest
```

### 2. Загрузка образа в registry
```bash
# Сначала залогиньтесь в registry
docker login YOUR_REGISTRY

# Затем запушьте образы
docker push YOUR_REGISTRY/superset-prod:4.1.1
docker push YOUR_REGISTRY/superset-prod:latest
```

## Развертывание в Kubernetes

### 1. Создайте namespace
```bash
kubectl create namespace superset
```

### 2. Создайте secrets для паролей
```bash
kubectl create secret generic superset-secrets \
  --from-literal=secret-key='CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET_KEY_HERE' \
  --from-literal=postgres-password='superset' \
  -n superset
```

### 3. Примените манифесты
```bash
kubectl apply -f k8s/ -n superset
```

### 4. Проверьте статус
```bash
kubectl get pods -n superset
kubectl get services -n superset
```

### 5. Получите URL для доступа
```bash
# Если используется LoadBalancer
kubectl get service superset -n superset

# Если используется NodePort
kubectl get nodes -o wide
# Используйте IP ноды и NodePort из сервиса
```

## Важные файлы

- `k8s/configmap.yaml` - Конфигурация Superset (pythonpath_prod/superset_config.py)
- `k8s/deployment.yaml` - Deployment с вашим кастомным образом
- `k8s/service.yaml` - Service для доступа
- `k8s/postgres.yaml` - PostgreSQL база данных
- `k8s/redis.yaml` - Redis для кеширования
- `k8s/ingress.yaml` - Ingress (опционально)

## Что включено в образ

✅ Кастомный логотип (80px)
✅ Поддержка русского и английского языков  
✅ Версия 4.1.1
✅ Production оптимизации
✅ Карта Kazakhstan
✅ CSV/Excel upload (настроено в конфиге)

## Первый вход

- URL: http://YOUR_SERVICE_URL:8088
- Логин: admin
- Пароль: admin

**ВАЖНО:** Измените пароль после первого входа!
