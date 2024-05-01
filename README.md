### Кроки  для запуска застосунка:

1. **Docker Compose Up:**
   Запустити Redis и PostgreSQL с допомогою Docker Compose:
   ```bash
   docker-compose up -d
2. **Alembic upgrade head:**
   Виконати міграцію:
   ```bash
   alembic upgrade heads
3. **Uvicorn main:app --reload:**
   Запустити сервер:
   ```bash
   python main.py