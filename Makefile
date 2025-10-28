
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

saas_models:
	datamodel-codegen \
	--url http://0.0.0.0:8088/api/schema/ \
	--capitalise-enum-members \
	--snake-case-field \
	--enum-field-as-literal=one \
	--use-double-quotes \
	--field-constraints \
	--output bot/saas/models.py \
