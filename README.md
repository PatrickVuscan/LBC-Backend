<h1 align="center">Welcome to LBC backend 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>


> This is a backend built using Python in combination with the [FastAPI](https://fastapi.tiangolo.com/) micro framework.

We highly recommend looking through the [docs](https://fastapi.tiangolo.com/tutorial/first-steps/) to get familiar with the framework as their documentation is fantastic.

### ✨ [Demo](https://lbc-backend-fxp5s3idfq-nn.a.run.app/docs) 

Please note that this Demo URL will expire by the end of January. There is no persistence given that we are using SQLite :cowboy_hat_face: as a temporary solution for testing persistence. Feel free to change the [Database URL](https://github.com/csc301-fall-2020/team-project-13-lady-ballers-camp-backend/blob/9ae4e562fdee0f78fcc27d6d3ef0185bce014e97/api/database/db_initialize.py#L6) to your own.

> Happy Coding :smile:

## Install

See [setup.md](https://github.com/csc301-fall-2020/team-project-13-lady-ballers-camp-backend/blob/master/setup.md)

## Run API Locally
```sh
export PYTHONPATH=. &&  python api/app.py
```

### API DOCS

Once server is running please visit [docs](http://0.0.0.0:8080/docs) to see how the API works. 

## Run tests

```sh
./scripts/run_tests.sh
```

## Build Docker Container

Before proceeding with Docker please make sure you install [Docker](https://docs.docker.com/get-docker/) for you machine.

```sh
./scripts/build_api_docker.sh
```

This will return an container ID. Then you will need to tag the container with `lbc-backend` as follows:

```sh
docker tag <container_id> lbc-backend
```

## Run Docker Container

Once you have tagged the container you are ready to run it locally as follows:

```sh
./scripts/run_docker.sh
```

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.

***
