# 📊 1C-Bitrix Observability Pack

[![CI](https://github.com/ranas-mukminov/onec-bitrix-observability-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/onec-bitrix-observability-pack/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🇷🇺 Русская версия | 🇬🇧 [English version](README.md)

Готовое решение для мониторинга типового стека российских предприятий: **1С:Предприятие**, **1C-Bitrix** и СУБД (PostgreSQL, MySQL, MS SQL Server). Набор включает экспортёры для Prometheus, дашборды Grafana, правила алертинга и AI-помощник для диагностики производительности критичных бизнес-систем.

## Основные возможности

- **Специализированные экспортёры** — Экспортёры Prometheus для метрик кластера 1С (сеансы, блокировки, фоновые задания) и Bitrix (PHP-FPM, кеш, компоненты)
- **Готовые дашборды** — Три уровня дашбордов Grafana: обзорная панель для руководителей, детальные панели для DBA/админов и инструменты глубокого анализа
- **Промышленный алертинг** — Правила Prometheus на основе методологии Four Golden Signals (задержка, трафик, ошибки, насыщение)
- **Мониторинг БД** — Интеграция с экспортёрами PostgreSQL, MySQL и MS SQL Server
- **AI-диагностика** — Модуль машинного обучения для детекции аномалий и рекомендаций на естественном языке
- **Готовность к контейнеризации** — Docker Compose для тестов, манифесты Kubernetes для продакшена
- **Приватность по умолчанию** — AI-помощник работает локально, без внешних вызовов API
- **Открытый код** — Лицензия Apache 2.0, кодовая база Python с полной типизацией

## Архитектура

```
Кластер 1С ────▶ onec_exporter ───┐
                                   │
Сайт Bitrix ───▶ bitrix_exporter ─┼──▶ Prometheus ──▶ Grafana
                                   │         │
СУБД ───────────▶ DB exporters ────┘         └──▶ Alertmanager
                                                      │
                                             AI Assistant
```

**Компоненты:**
- **Exporters**: Собирают метрики из 1С (RAS API), Bitrix (PHP-FPM/Nginx) и БД
- **Prometheus**: База временных рядов, опрашивает экспортёры каждые 15 секунд
- **Grafana**: Визуализация с преднастроенными дашбордами
- **Alertmanager**: Маршрутизация уведомлений (email/Slack/PagerDuty)
- **AI Assistant**: Анализ паттернов, детекция аномалий, генерация рекомендаций

## Требования

**ОС**: Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+  
**Железо**: 2+ ядра CPU, 4 ГБ RAM (8 ГБ с AI-модулем), 20 ГБ диск  
**ПО**: Docker 20.10+ и Compose 2.0+ ИЛИ Python 3.10+  
**Сеть**: Доступ к RAS-порту 1С (1545), портам БД, исходящий трафик на Docker Hub/PyPI  
**Права**: sudo для Docker, роль ClusterAdmin в 1С, read-only пользователь БД

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/ranas-mukminov/onec-bitrix-observability-pack.git
cd onec-bitrix-observability-pack

# Настроить параметры подключения
cp docker-compose.example.yml docker-compose.yml
nano docker-compose.yml  # Отредактировать ONEC_CLUSTER_HOST, учётные данные, строку подключения к БД

# Запустить стек мониторинга
docker-compose up -d

# Открыть интерфейсы
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# Метрики 1С: http://localhost:8000/metrics
```

Импорт дашбордов: Grafana → Dashboards → Import → Выбрать файлы из `dashboards/grafana/`

## Установка

### Docker Compose (рекомендуется)

```bash
# Установить Docker
sudo apt-get install -y docker.io docker-compose  # Ubuntu/Debian
sudo dnf install -y docker docker-compose && sudo systemctl enable --now docker  # RHEL/Rocky

# Развернуть
docker-compose up -d

# Проверить
docker-compose ps
curl http://localhost:8000/metrics | head
```

### Kubernetes

```bash
# Создать namespace
kubectl create namespace monitoring

# Настроить секреты
kubectl create secret generic onec-credentials \
  --from-literal=username=admin \
  --from-literal=password=<ВАШ_ПАРОЛЬ> \
  -n monitoring

# Развернуть экспортёры
kubectl apply -f examples/k8s/deployment_onec_exporter.yaml
kubectl apply -f examples/k8s/deployment_bitrix_exporter.yaml

# Установить стек Prometheus (Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

Обновить ConfigMap Prometheus, добавив цели сбора метрик из `examples/prometheus/prometheus.yml`.

### Нативная установка (Ubuntu/Debian)

```bash
# Установить зависимости
sudo apt-get install -y python3.10 python3-pip

# Установить экспортёр 1С
cd exporters/onec
pip3 install .

# Создать systemd-сервис
sudo tee /etc/systemd/system/onec-exporter.service > /dev/null <<EOF
[Unit]
Description=1C Prometheus Exporter
After=network.target

[Service]
Type=simple
User=prometheus
Environment="ONEC_CLUSTER_HOST=<ВАШ_СЕРВЕР_1С>"
Environment="ONEC_ADMIN_USER=<ЛОГИН>"
Environment="ONEC_ADMIN_PASSWORD=<ПАРОЛЬ>"
ExecStart=/usr/local/bin/onec-exporter
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now onec-exporter
```

## Настройка

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `ONEC_CLUSTER_HOST` | IP-адрес сервера кластера 1С | Обязательно |
| `ONEC_CLUSTER_PORT` | Порт RAS | `1545` |
| `ONEC_ADMIN_USER` | Имя администратора кластера | Обязательно |
| `ONEC_ADMIN_PASSWORD` | Пароль администратора | Обязательно |
| `PROMETHEUS_LISTEN_PORT` | HTTP-порт экспортёра | `8000` |
| `LOG_LEVEL` | DEBUG/INFO/WARNING | `INFO` |

### Конфигурация Prometheus

```yaml
scrape_configs:
  - job_name: 'onec_exporter'
    static_configs:
      - targets: ['onec_exporter:8000']
        labels:
          cluster: 'production'

  - job_name: 'bitrix_exporter'
    static_configs:
      - targets: ['bitrix_exporter:8080']
```

## Использование

**Управление сервисами:**
```bash
docker-compose up -d          # Запустить все
docker-compose restart onec_exporter  # Перезапустить один
docker-compose logs -f grafana        # Просмотр логов
docker-compose down           # Остановить все
```

**Доступ к мониторингу:**
- Grafana: `http://<IP_СЕРВЕРА>:3000`
- Prometheus: `http://<IP_СЕРВЕРА>:9090`

**Примеры PromQL-запросов:**
```promql
# Активные сеансы 1С
onec_cluster_sessions_active{cluster="production"}

# Скорость запросов PHP-FPM в Bitrix
rate(bitrix_phpfpm_requests_total[5m])
```

**AI-помощник:**
```bash
docker-compose exec ai_assistant python -m ai_assistant.cli \
  --prometheus-url http://prometheus:9090 \
  --query "onec_cluster_sessions_active > 100" \
  --time-range 1h
```

## Обновление

```bash
# Бэкап конфигурации
cp docker-compose.yml docker-compose.yml.backup

# Получить обновления
git pull origin main

# Пересобрать контейнеры
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Проверить
curl http://localhost:8000/metrics
```

## Устранение неполадок

**Проблема**: Экспортёр 1С показывает "Connection Refused"  
**Решение**: Проверить `ONEC_CLUSTER_HOST`, убедиться что RAS работает (`telnet <HOST> 1545`), проверить фаервол.

**Проблема**: Нет данных в Grafana  
**Решение**: Проверить цели Prometheus (`http://localhost:9090/targets`), проверить метрики экспортёра (`curl http://localhost:8000/metrics`).

**Проблема**: Порт 8000 уже занят  
**Решение**: Изменить порт в `docker-compose.yml`: `ports: - "8001:8000"`

**Просмотр логов:**
```bash
docker-compose logs --tail=100 -f onec_exporter
sudo journalctl -u onec-exporter -f  # systemd
```

## Безопасность

- **Сменить пароли по умолчанию**: `docker-compose exec grafana grafana-cli admin reset-admin-password <НОВЫЙ_ПАРОЛЬ>`
- **Ограничить доступ**: Использовать правила фаервола, НЕ выставлять порты 8000/8080/9090 в Интернет
- **Включить HTTPS**: Использовать Nginx/Traefik reverse proxy с Let's Encrypt
- **Использовать секреты**: Хранить учётные данные в Docker/Kubernetes secrets, не в plaintext
- **Read-only пользователи БД**: Экспортёрам нужны только права SELECT
- **Регулярные обновления**: `docker-compose pull && docker-compose up -d`

## Структура проекта

```
exporters/          # Экспортёры Prometheus (onec, bitrix)
dashboards/grafana/ # JSON-дашборды Grafana (обзор, админ, детальный)
alerts/prometheus/  # Правила алертинга YAML
ai/                 # Модуль AI-диагностики
examples/           # Примеры конфигов (prometheus.yml, манифесты k8s)
scripts/            # Скрипты CI/тестирования
tests/              # Unit и интеграционные тесты
docker-compose.example.yml  # Шаблон полного стека
```

## Участие в разработке

1. Форк и клонирование: `git clone https://github.com/<ВАШ_USER>/onec-bitrix-observability-pack.git`
2. Создать ветку: `git checkout -b feature/my-feature`
3. Запустить тесты: `./scripts/dev_run_all_tests.sh`
4. Коммит: `git commit -m "Добавить функцию"`
5. Push и открыть PR

**Стандарты кода**: PEP 8, type hints, форматирование `black`, покрытие тестами 80%+. См. [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

Apache License 2.0. См. [LICENSE](LICENSE) и [LEGAL.md](LEGAL.md) для подробностей.

**Основные положения**: Свободно для коммерческого использования, разрешена модификация, без гарантий.

## Автор и коммерческая поддержка

**Автор**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Сайт**: [run-as-daemon.ru](https://run-as-daemon.ru)

### Профессиональные услуги

Доступна коммерческая поддержка для продакшн-внедрений:
- Настройка мониторинга 1С/Bitrix «под ключ»
- Разработка кастомных дашбордов и настройка алертинга
- Аудит производительности и консалтинг по оптимизации
- Обучение команды SRE/DevOps лучшим практикам мониторинга
- Контракты на круглосуточную поддержку

Обращайтесь через [run-as-daemon.ru](https://run-as-daemon.ru) или GitHub issues.

## Дисклеймер

НЕ является официальным продуктом фирмы «1С» или «1С-Битрикс». Предоставляется «как есть», без гарантий. Пользователь несёт ответственность за настройку и соблюдение требований законодательства о защите данных (152-ФЗ, GDPR). См. [LEGAL.md](LEGAL.md).
