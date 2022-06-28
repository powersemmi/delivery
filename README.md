# Инструкция по запуску
Все инструкции требуется выполнять находясь в директории проекта.
Все команды нужно выполнять находять в корне проекта.
Для Windows выполнять команды следует из среды powershell или wsl2

1. Нужно скачать и установить следующие компоненты:
    * python3.10
    * docker
    * docker-compose
2. Выполнить следующие команды для запуска:
    * python -m pip install pipenv
    * python -m pipenv sync
    * docker-compose up -d // для запуска postgres
    * cp example.env .env
    * python -m pipenv run migrate
    * python -m pipenv run load // для загрузки датасета в бд
    * python -m pipenv run run-server // для запуска сервера