# API Ingestor (Python + PostgreSQL + Docker Compose)

Сервис раз в **N минут** запрашивает данные из публичного API (в проекте — погода через **Open-Meteo**, без API-ключа), обрабатывает ответ и сохраняет результат в PostgreSQL.

Данные сохраняются в две связанные таблицы:
- `requests` — история запросов (endpoint, параметры, статус, длительность, ошибка)
- `responses` — полезные данные ответа + `raw_json`, связаны с `requests` через внешний ключ `request_id`

Ошибки подключения/таймаутов и ошибки БД логируются в отдельный файл `./logs/errors.log`.

---

## Требования

- Docker Desktop (Mac/Windows/Linux)
- `docker compose`

---

## Быстрый старт

1) Создайте файл окружения:
```bash
cp .env.example .env
```
Запустите проект:
```bash
docker compose up --build
```
Контейнеры:
```bash
api_ingestor_db — PostgreSQL
api_ingestor_app — Python-скрипт (вечный цикл: запрос → сохранение → sleep)
```
Логи ошибок: 
```bash 
./logs/errors.log
```
## Проверка, что всё работает
1) Проверить, что запросы пишутся
```bash
docker exec -it api_ingestor_db psql -U app -d app -c "SELECT COUNT(*) FROM requests;"
```
2) Посмотреть последние запросы
```bash
docker exec -it api_ingestor_db psql -U app -d app -c "
SELECT id, requested_at, status_code, duration_ms, error
FROM requests
ORDER BY requested_at DESC
LIMIT 5;
"
```
3) Посмотреть JOIN (история + данные ответа)
```bash
docker exec -it api_ingestor_db psql -U app -d app -c "
SELECT
  r.id,
  r.requested_at,
  r.endpoint,
  r.params,
  r.status_code,
  r.duration_ms,
  r.error,
  s.temperature_2m,
  s.wind_speed_10m,
  s.raw_json
FROM requests r
LEFT JOIN responses s ON s.request_id = r.id
ORDER BY r.requested_at DESC
LIMIT 10;
"
```
## SQL-запрос с JOIN (для проверки вручную в psql)
Если подключаетесь в psql интерактивно:
```bash
docker exec -it api_ingestor_db psql -U app -d app
SQL:
SELECT
  r.id,
  r.requested_at,
  r.endpoint,
  r.params,
  r.status_code,
  r.duration_ms,
  r.error,
  s.temperature_2m,
  s.wind_speed_10m,
  s.raw_json
FROM requests r
LEFT JOIN responses s ON s.request_id = r.id
ORDER BY r.requested_at DESC;
```
## Переменные окружения (.env)
### PostgreSQL
#### POSTGRES_DB — имя БД
#### POSTGRES_USER — пользователь
#### POSTGRES_PASSWORD — пароль
#### POSTGRES_HOST — хост (в docker-compose: db)
#### POSTGRES_PORT — порт PostgreSQL внутри docker-сети (обычно 5432)

## Параметры опроса API
#### FETCH_INTERVAL_MINUTES — интервал опроса (минуты)
#### HTTP_TIMEOUT_SECONDS — таймаут HTTP-запроса (секунды)
#### API_BASE_URL — endpoint публичного API (по умолчанию Open-Meteo)
#### LATITUDE, LONGITUDE, TIMEZONE — параметры запроса
## Логи
ERROR_LOG_PATH — путь к файлу логов ошибок (по умолчанию /app/logs/errors.log, на хосте это ./logs/errors.log)