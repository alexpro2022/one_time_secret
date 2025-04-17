## Виртуальное окружение:
<details><summary>Среда разработки</summary><br>

1. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS:
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows:
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```
```bash
where python
```

<br>

2. Установите в виртуальное окружение необходимые зависимости:
```bash
python -m venv .venv && \
. .venv/Scripts/activate && \
python.exe -m pip install --upgrade pip && \
python -m pip install -e .[test]  && \
pytest
```
    Сохранить зависимости в файл и отредактировать файлы в `requirements/`:
    ```bash
    pip freeze > requirements/requirements.txt
    ```
<br>

Миграции БД делаются в `sqlite+aiosqlite`.
1. Для этого раскомментировать в файле alembic/.env.py:
```py
config.set_main_option('sqlalchemy.url', "sqlite+aiosqlite:///./temp.db")
```
2. Создать файл миграций командой:
```bash
alembic revision --autogenerate
```
3. Добавить в этот файл
```py
import sqlmodel
```
4. Закомментировать строку из пункта 1.


### Normally the development is in Docker, below is exceptional development:
3. Запуск тестов - после прохождения тестов в консоль будет выведен отчет `pytest` и `coverage`(**xx%**):
```bash
pytest
```
<br>

4. Запуск приложения - проект будет развернут по адресу http://127.0.0.1:8000:
```bash
uvicorn src.app:app --reload
python start_app.py
```
<br>

5. Остановить приложение можно комбинацией клавиш `CTRL+C`.

[⬆️Оглавление](#оглавление)

---

</details>
<br>
