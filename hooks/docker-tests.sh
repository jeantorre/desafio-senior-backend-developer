#!/bin/bash
echo "Executando testes no container..."

CONTAINER_ID=$(docker ps --filter "name=backend-desafio-dev" --format "{{.ID}}")

if [ -z "$CONTAINER_ID" ]; then
  echo "Error: Container backend-desafio-dev não foi encontrado"
  echo "Por favor, inicie o container antes de commitar"
  exit 1
fi

echo "Executando testes no container $CONTAINER_ID"
docker exec $CONTAINER_ID pytest -v tests/

exit $?
