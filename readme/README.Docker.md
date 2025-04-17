## Разработка в Docker:
<details><summary>Запуск приложения</summary><br>
   <details><summary>Предварительные условия</summary><br>

   Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

   ```bash
   docker -v && docker compose version
   ```

   ---

   </details>
<br>

<!-->
Миграция БД
```bash
docker compose -f docker/dev/migration.docker-compose.yaml --env-file .env up --build --detach
docker compose -f docker/dev/migration.docker-compose.yaml --env-file .env down && docker system prune -f
docker compose -f docker/dev/migration.docker-compose.yaml --env-file .env down -v && docker system prune -f
```
<-->

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
# docker compose -f docker/dev/docker-compose.yaml --env-file .env up --watch
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

---

</details>
<br>


# Simple python docker dev example for the official docker docs
https://docs.docker.com/language/python/develop/


### Building and running your application

1. Start application:
```bash
docker compose up --build
docker compose up --build -d
```
Application will be available at http://localhost:8001.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
