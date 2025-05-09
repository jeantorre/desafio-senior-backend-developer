export ENVIRONMENT=dev
docker compose --env-file .env.${ENVIRONMENT} -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml up --build
