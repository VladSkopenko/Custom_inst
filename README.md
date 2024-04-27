### Кроки  для запуска застосунка:

1. **Docker Compose Up:**
   Запустити Redis и PostgreSQL с допомогою Docker Compose:
   ```bash
   docker-compose up -d
2. **Alembic upgrade head:**
   Виконати міграцію:
   ```bash
   alembic upgrade head
3. **Uvicorn main:app --reload:**
   Запустити сервер:
   ```bash
   uvicorn main:app --reload