# TaskFlow

TaskFlow — учебное веб-приложение для управления проектами, задачами и файлами.

## Возможности

- регистрация пользователей
- авторизация пользователей
- создание проектов
- редактирование и удаление проектов
- создание задач внутри проектов
- редактирование, удаление и завершение задач
- загрузка файлов к задачам
- хранение данных в SQLite
- REST API для проектов и задач
- оформление через Bootstrap
- работа с HTML-шаблонами Jinja2

## Использованные технологии

- Python
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- SQLite
- Bootstrap
- REST API
- Git

## Структура проекта

```text
taskflow_project/
├── app.py
├── requirements.txt
├── data/
├── forms/
├── routes/
├── templates/
├── static/
├── docs/
└── instance/
```

## Запуск на macOS и Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

После запуска открыть:

```text
http://127.0.0.1:8080
```

## Запуск на Windows

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

После запуска открыть:

```text
http://127.0.0.1:8080
```

## REST API

API доступно только авторизованному пользователю.

### Получить проекты

```text
GET /api/projects
```

### Получить один проект

```text
GET /api/projects/<id>
```

### Получить задачи

```text
GET /api/tasks
```

### Получить одну задачу

```text
GET /api/tasks/<id>
```

### Создать задачу

```text
POST /api/tasks
```

Пример JSON:

```json
{
  "title": "Сделать презентацию",
  "description": "Подготовить слайды для защиты",
  "project_id": 1,
  "status": "Новая",
  "priority": "Высокий"
}
```

### Удалить задачу

```text
DELETE /api/tasks/<id>
```

## Роли участников

### Участник 1

Backend, база данных, авторизация, модели SQLAlchemy.

### Участник 2

HTML-шаблоны, Bootstrap, страницы, загрузка файлов.

### Участник 3

REST API, README, пояснительная записка, презентация, проверка проекта.

## Инструкция сдачи

1. Создать git-репозиторий.
2. Загрузить все файлы проекта.
3. Добавить преподавателю доступ.
4. Проверить запуск проекта.
5. Приложить ссылку на репозиторий в качестве решения.
