#!/bin/bash

source ../variables.env
set -x

POSTGRES_CONTAINER_NAME="local_pgdb"
DATABASE_DIR="$(pwd)"

echo "rechten fixen..."
sudo chown -R 999:999 ${DATABASE_DIR}/postgres_data
sudo chown -R 5050:5050 ${DATABASE_DIR}/pgadmin_data
sudo chmod -R 700 ${DATABASE_DIR}/postgres_data
sudo chmod -R 700 ${DATABASE_DIR}/pgadmin_data

echo "containers herstarten..."
sudo docker-compose down
sudo docker-compose up -d

echo "even wachten..."
sleep 30

# Wijzig de 'administrator' rol, stel wachtwoord in en maak superuser
docker exec -i $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
"ALTER ROLE $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD' SUPERUSER;"


  #Met SERIAL wordt een kolom gemaakt die automatisch wordt geïncrementeerd#
docker exec -i $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
"ALTER SCHEMA public OWNER TO $POSTGRES_USER;
CREATE TABLE IF NOT EXISTS public.auth_log (

  id SERIAL PRIMARY KEY,
  timestamp timestamp NOT NULL,
  \"user\" text,
  source_ip varchar,
  hostname text NOT NULL,
  event_type text,
  full_event text NOT NULL
);
ALTER TABLE public.auth_log OWNER TO $POSTGRES_USER;"

echo "Klaar. Ga naar http://IP_address:8888. Login met: $PGADMIN_DEFAULT_EMAIL"
