# Chime backend
![](https://github.com/Chime-Menu/chime-backend/workflows/MyAppRest%20unit%20tests/badge.svg)

## Installation & Running

**Note**: `Python 3.7.3` required

1. Install PyCharm (professional version is free for students)
2. Clone repository
3. Install docker and docker compose
4. Confirm unit tests run successfully with `docker-compose -f docker-compose.test.yml -p MyAppRest-tests up --exit-code-from tests --force-recreate --build`
5. Set up the virtual environment
6. `pip install -r requirements.txt` in virtualenv
7. Run `Run bg services`. To ensure BG services started successfully go to services, and check the logs for each container. Usually take 60sec to fully initialize.
8. Run `Create db`. Double check that the schema was created (`postgresql://serviceclient:password@localhost:5433/chimedb`)
9. Run `Run Chime dev`. Ensure that services started up correctly.

## Services

### `Postgres`
Can reset the postgres database by deleting the .postgres folder (`rm -rf .postgres`). Make sure to you stop the postgres container before doing this and you restart it after.

### `MyAppRest`
[REST API](https://documenter.getpostman.com/view/4393306/SztEanZE?version=latest) for Chime. Currently at `http://localhost:5000`
