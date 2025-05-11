export ENVIRONMENT=prod
docker compose --env-file .env.${ENVIRONMENT} -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml up -d --build
