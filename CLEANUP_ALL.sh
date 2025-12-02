#!/bin/bash
# Полная очистка проекта для production передачи DevOps

echo "🧹 ПОЛНАЯ ОЧИСТКА ПРОЕКТА ДЛЯ PRODUCTION"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# ============================================================
# 1. УДАЛЕНИЕ ЛИШНИХ ФАЙЛОВ В ROOT
# ============================================================
echo "📁 Шаг 1: Очистка корневой директории..."

# Удаляем dev/test файлы и папки
rm -rf .github .devcontainer .cursor .claude tests
rm -rf docs scripts cypress-base
rm -rf CHANGELOG ASF RELEASING RESOURCES

# Удаляем dev конфигурацию
rm -f .pre-commit-config.yaml .pylintrc .codecov.yml .coveragerc
rm -f .markdownlint.json .rat-excludes .fossa.yml
rm -f AGENTS.md CLAUDE.md CODE_OF_CONDUCT.md CONTRIBUTING.md
rm -f LINTING_ARCHITECTURE.md INSTALL.md UPDATING.md
rm -f lintconf.yaml Makefile

# Удаляем dev Docker файлы
rm -f Dockerfile dockerize.Dockerfile
rm -f docker-compose*.yml

# Удаляем примеры
rm -rf superset/examples

# Удаляем лишние модули
rm -rf superset-websocket superset-embedded-sdk superset-extensions-cli

# Удаляем временные/тестовые файлы
rm -f nul GEMINI.md GPT.md

# Удаляем дубликат папки
rm -rf "docker-prod;C"

# Удаляем helm (для K8s используем наши манифесты)
rm -rf helm

echo "  ✅ Корневая директория очищена"

# ============================================================
# 2. ОЧИСТКА docker-prod
# ============================================================
echo ""
echo "📁 Шаг 2: Очистка docker-prod..."

cd docker-prod

# Удаляем временные и dev файлы
rm -f build.log
rm -f current_logo_check.png
rm -f custom.css
rm -f superset-logo-horiz.png
rm -f geo2topo.js
rm -f README.md

# Удаляем дубликат папки
rm -rf "geojson;C"

# Очистка geojson папки - оставляем только нужные файлы
if [ -d "geojson" ]; then
    cd geojson
    echo "  Очистка geojson папки..."
    rm -f kaz_adm1_regions_fixed.geojson
    rm -f kaz_adm2_districts_fixed.geojson
    rm -f kaz_districts.topo.json
    rm -f kaz_regions.topo.json
    cd ..
fi

# Удаляем init-db (не нужна для production)
rm -rf init-db

cd ..

echo "  ✅ docker-prod очищен"

# ============================================================
# 3. ОЧИСТКА superset-frontend
# ============================================================
echo ""
echo "📁 Шаг 3: Очистка superset-frontend..."

cd superset-frontend

# Удаляем node_modules и кэш (будет пересобрано при build)
rm -rf node_modules .cache

# Удаляем временные файлы
rm -rf coverage .nyc_output

cd ..

echo "  ✅ superset-frontend очищен"

# ============================================================
# ИТОГОВАЯ СТАТИСТИКА
# ============================================================
echo ""
echo "========================================"
echo "✅ ОЧИСТКА ЗАВЕРШЕНА!"
echo "========================================"
echo ""
echo "📊 Что осталось в проекте:"
echo ""
echo "Важные файлы:"
ls -lh README_PROD.md ПЕРЕДАТЬ_DEVOPS.txt 2>/dev/null | awk '{print "  " $9 " - " $5}'
echo ""
echo "Основные папки:"
du -sh docker-prod superset superset-frontend superset-core requirements 2>/dev/null | awk '{print "  " $2 " - " $1}'
echo ""
echo "docker-prod содержит:"
ls -1 docker-prod/ | grep -v '^total' | awk '{print "  - " $0}'
echo ""
echo "🎯 Проект готов к передаче DevOps!"
