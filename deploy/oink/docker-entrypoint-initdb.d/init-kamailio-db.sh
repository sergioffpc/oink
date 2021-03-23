#! /bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER kamailio WITH PASSWORD 'kamailio';
  CREATE DATABASE kamailio;
  GRANT ALL PRIVILEGES ON DATABASE kamailio TO kamailio;
EOSQL

psql -v ON_ERROR_STOP=1 --username kamailio --dbname kamailio -f /docker-entrypoint-initdb.d/init-kamailio/init-kamailio-ddl.sql
psql -v ON_ERROR_STOP=1 --username kamailio --dbname kamailio -f /docker-entrypoint-initdb.d/init-kamailio/init-kamailio-dml.sql
