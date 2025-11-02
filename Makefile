
# Собрать и запустить проект
up:
	docker-compose up --build

# Только собрать образы
build:
	docker-compose build

# Остановить контейнеры
down:
	docker-compose down

down-v:
	docker-compose down -v

# Посмотреть логи
logs:
	docker-compose logs -f

# Перезапустить проект
restart: down up


cfile:
	curl http://0.0.0.0:8088/api/schema/ -o schema.json

cmodels:
	datamodel-codegen --input schema.json --input-file-type openapi \
	  --output-model-type pydantic_v2.BaseModel \
	  --capitalise-enum-members \
	  --snake-case-field \
	  --enum-field-as-literal=one \
	  --use-double-quotes \
	  --target-python-version 3.12 \
	  --disable-timestamp \
	  --output bot/saas/models.py
