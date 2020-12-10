# OINK!
The `oink` project is an environment lab to experiment the `Kazoo` system.

## Build and initialization
To build the `oink` project you need to run the following command inside the `deploy/oink/` directory.

```buildoutcfg
docker-compose build
```

After the build you need to start the containers using the following command.

```buildoutcfg
docker-compose up
```

Then execute the `post-install.sh` script inside the `deploy/oink/` directory to initialize the environment.

## Run
To start the `oink` project you need to run the following command.

```buildoutcfg
docker-compose start
```

To stop the `oink` project you need to run the following command.

```buildoutcfg
docker-compose stop
```

## Exposed services
### API
The `oink` project exposes the `Kazoo` API through URL http://localhost:8000/v2/ .

### Web interface
The `oink` project exposes the `Kazoo` web-based interface trough http://localhost using `oink` as username, password and account name.

## RabbitMQ
The RabbitMQ exposes monitoring tools through http://localhost:15672/ using `guest` as username and password.

## CouchDB
The CouchDB exposes a web-based interface through http://localhost:5984/_utils/ using `couchdb` as username and password.
