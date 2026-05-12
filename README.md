# ✅ Task Manager API

Асинхронный REST API для управления задачами с JWT авторизацией, кешированием через Redis и хранением данных в PostgreSQL.

## 🚀 Стек технологий

- **FastAPI** — асинхронный веб-фреймворк
- **PostgreSQL** — основная база данных
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции базы данных
- **Redis** — кеширование задач (Cache-Aside паттерн)
- **JWT** — авторизация через токены
- **Docker / Docker Compose** — контейнеризация
- **Pydantic** — валидация данных
- **pytest** — тестирование с тестовой БД

## ⚙️ Функциональность

- Регистрация и авторизация пользователей через JWT
- Создание, получение, обновление и удаление задач
- Каждый пользователь видит и управляет только своими задачами
- Кеширование задач через Redis с автоматической инвалидацией
- Частичное обновление задач через PATCH
- Тесты с отдельной тестовой БД

## 📁 Структура проекта

```
task-manager/
├── app/
│   ├── main.py              # Точка входа, lifespan
│   ├── config.py            # Настройки через pydantic-settings
│   ├── database.py          # Async подключение к БД
│   ├── redis_client.py      # Redis клиент
│   ├── models/
│   │   ├── base.py          # Base для SQLAlchemy
│   │   ├── user.py          # Модель пользователя
│   │   └── task.py          # Модель задачи
│   ├── repositories/
│   │   ├── user.py          # Слой работы с пользователями
│   │   └── task.py          # Слой работы с задачами
│   ├── services/
│   │   └── auth.py          # JWT логика, хеширование паролей
│   ├── routers/
│   │   ├── auth.py          # Эндпоинты авторизации
│   │   └── task.py          # Эндпоинты задач
│   └── schemas/
│       ├── auth.py          # Pydantic схемы пользователя
│       └── task.py          # Pydantic схемы задачи
├── migrations/              # Alembic миграции
├── tests/
│   ├── conftest.py          # Фикстуры с тестовой БД
│   ├── test_auth.py         # Тесты авторизации
│   └── test_tasks.py        # Тесты задач
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## 🛠️ Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/eternal-silence00/Task-Manager.git
cd Task-Manager
```

### 2. Создать `.env` файл

```properties
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/taskmanager
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=taskmanager
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 3. Запустить через Docker

```bash
docker-compose up --build
```

### 4. Применить миграции

```bash
docker-compose exec app alembic upgrade head
```

### 5. Открыть документацию

```
http://localhost:8000/docs
```

## 📮 API Endpoints

### Авторизация

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/auth/register` | Регистрация пользователя |
| `POST` | `/auth/login` | Вход и получение JWT токена |

### Задачи (требуют JWT токен)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/task` | Получить все свои задачи |
| `POST` | `/task` | Создать задачу |
| `GET` | `/task/{task_id}` | Получить задачу по ID |
| `PATCH` | `/task/{task_id}` | Обновить задачу |
| `DELETE` | `/task/{task_id}` | Удалить задачу |

### Примеры запросов

**Регистрация:**
```json
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Создание задачи:**
```json
POST /task
Authorization: Bearer <token>
{
  "title": "Купить продукты",
  "description": "Молоко, хлеб, яйца"
}
```

**Частичное обновление:**
```json
PATCH /task/1
Authorization: Bearer <token>
{
  "status": "Done"
}
```

## 🧠 Архитектурные решения

**JWT авторизация** — stateless аутентификация. Каждый запрос содержит токен с `user_id`. Сервер не хранит сессии.

**Cache-Aside паттерн** — при запросе задачи сначала проверяется Redis. Кеш инвалидируется при создании, изменении и удалении задач.

**Авторизация на уровне данных** — перед любой операцией с задачей проверяется что `task.user_id == current_user.id`. Пользователь не может получить доступ к чужим задачам.

**Repository паттерн** — слой репозитория отделяет бизнес-логику от работы с БД.

## 🧪 Запуск тестов

```bash
docker-compose exec app pytest tests/ -v
```

Тесты используют отдельную БД `taskmanager_test` и не затрагивают основные данные.