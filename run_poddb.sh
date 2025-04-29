source .env
echo $DB_PASSWORD
podman stop poddb.$DOMAIN
podman rm poddb.$DOMAIN
podman volume rm podmandb
podman volume create podmandb
podman secret rm pmk_env
podman secret create pmk_env ./.env
podman run -d \
  --name poddb.$DOMAIN \
  --secret=pmk_env \
  -v podmandb:/var/lib/pgsql/data:Z \
  -e POSTGRES_PASSWORD=PASSWORD \
  -p 5433:5432 \
  postgres:latest 


