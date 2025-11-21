# onec-bitrix-observability-pack

## English

**onec-bitrix-observability-pack** is a comprehensive observability suite designed for the typical Russian enterprise technology stack: **1C:Enterprise**, **1C-Bitrix**, and their underlying databases (PostgreSQL, MySQL, SQL Server). It provides exporters, Grafana dashboards, Prometheus alerts, and an AI-powered assistant to help diagnose performance issues.

This project aims to provide a "batteries-included" monitoring solution for SREs and DevOps engineers managing 1C and Bitrix environments.

---

## Русский

**onec-bitrix-observability-pack** — это готовый набор инструментов для мониторинга типового стека российских предприятий: **1С:Предприятие**, **1C-Bitrix** и СУБД.

### Что это
*   Комплект экспортёров для Prometheus.
*   Типовые дашборды Grafana (для директоров, админов, глубокого анализа).
*   Набор правил для алертинга (Alertmanager).
*   AI-помощник для интерпретации метрик и поиска узких мест.

### Для кого
*   Интеграторы 1С/Bitrix.
*   Внутренние IT/DevOps команды.
*   Компании SMB сектора, где стабильность 1С/Bitrix критична для бизнеса.

### Как запустить (быстрый старт)
См. `docker-compose.example.yml` для быстрого развертывания полного стека мониторинга.

### Профессиональные услуги – run-as-daemon.ru

Проект развивается DevOps/DevSecOps-инженером с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вам нужно:
- настроить мониторинг 1С+Bitrix «под ключ»;
- внедрить алерты и дашборды для директоров и админов;
- разобрать хронические проблемы производительности,

вы можете заказать консалтинг, внедрение и поддержку.

### Ограничения / Дисклеймер
*   Не является официальным продуктом 1С или Bitrix.
*   Примеры конфигов и данных — синтетические.
*   Ответственность за корректность настройки и интерпретацию метрик лежит на пользователе.
