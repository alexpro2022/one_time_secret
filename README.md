# One time secret

[![CI/CD](https://github.com/alexpro2022/one_time_secret/actions/workflows/flow_ci_cd.yaml/badge.svg)](https://github.com/alexpro2022/one_time_secret/actions/workflows/flow_ci_cd.yaml)
[![Test Suite](https://github.com/alexpro2022/one_time_secret/actions/workflows/flow_branch_test.yaml/badge.svg)](https://github.com/alexpro2022/one_time_secret/actions/workflows/flow_branch_test.yaml)


#### Задание:
Разработать HTTP-сервис на FastAPI, в котором можно хранить конфиденциальные данные (далее — «секреты»).
  * Все «секреты» должны храниться в зашифрованном виде (не в открытом тексте).
  * По истечении заданного срока (ttl_seconds) «секрет» становится недоступен. Необходимо обеспечить периодическую или событийную очистку просроченных секретов (с учётом кеша).
  * Секрет обязательно должен выдаваться только один раз: после первого запроса к нему по уникальному ключу он становится недоступным.
	- После первого прочтения «секрет» не должен более возвращаться.
	- При удалении по запросу пользователя «секрет» также становится недоступен.

<br>


## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Виртуальное окружение](#виртуальное-окружение)
- [Разработка в Docker](#Разработка-в-Docker)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>


## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/pydantic-2-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=codecov)](https://pytest-cov.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

---

</details>
<br>


## Описание работы:

Проект развернут на удаленном сервере.
Техническая документация:
  - Swagger: http://185.221.162.231:9000/docs
  - Redoc: http://185.221.162.231:9000/redoc


Для разработки используются эндпойнты по адресу:
http://185.221.162.231:9000/docs#/Development<br>
Сервисные эндпойнты по адресу:
http://185.221.162.231:9000/docs#/Secrets<br>
Администрирование БД может быть осуществлено через админ панель по адресу:
http://185.221.162.231:9001<br>
Учетные данные для входа в админ-зону:<br>
Пароль: `postgres`<br>
![alt text](images/credentials.png)

[⬆️Оглавление](#оглавление)

<br>


## Установка приложения:
Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/one_time_secret.git
cd one_time_secret
cp .env.example .env
nano .env
```
Все последующие команды производятся из корневой директории проекта.

[⬆️Оглавление](#оглавление)

<br>


## Разработка в Docker:
   <details><summary>Предварительные условия</summary><br>

   Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

   ```bash
   docker -v && docker compose version
   ```

   ---

   </details>
<br>

1. Запуск тестов - после прохождения тестов в консоль будет выведен отчет `pytest` и `coverage`(**xx%**):
```bash
docker compose -f docker/dev/test.docker-compose.yaml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/dev/test.docker-compose.yaml --env-file .env down --volumes && docker system prune -f
```
<br>

2. Запуск приложения - проект будет развернут в docker-контейнерах по адресу http://localhost:9000/docs:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env up --build --detach
```
Для работы удобно использовать режим режим разработки:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env watch --prune --quiet
```
<br>

3. Остановить docker и удалить контейнеры можно командой:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env down && docker system prune -f
```

Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env down --volumes && docker system prune -f
```

[⬆️Оглавление](#оглавление)


<br>


## Удаление приложения:
```bash
cd .. && rm -fr one_time_secret
```

[⬆️Оглавление](#оглавление)

<br>


## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#project_name)
