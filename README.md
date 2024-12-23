# Команды для работы с проектом

## Общая информация
Этот файл описывает полезные команды для работы с проектом с использованием [Just](https://github.com/casey/just). Ниже приведены описания каждой команды и их назначение.

---

### Поднять весь проект в Docker
```bash
just up
```
Поднимает весь проект, включая API и PostgreSQL.

- **Команда:** 
  ```bash
  docker compose --profile api \
    --profile postgres_db up --build -d
  ```

---

### Запуск приложения
```bash
just run
```
Запускает приложение.

- **Команда:** `just _py python -Om src`

---

### Установка пакетов с зависимостями
```bash
just install
```
Устанавливает все зависимости проекта.

- **Команда:** `uv sync --all-groups`

---

### Проверка кода
```bash
just lint
```
Запускает pre-commit для проверки всех файлов.

- **Команда:** `just _py pre-commit run --all-files`

---

### Запуск тестов
```bash
just test
```
Запускает тесты с использованием Pytest.

---
