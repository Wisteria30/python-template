#################################################################################
# GLOBALS                                                                       #
#################################################################################
# 環境変数IN_CONTAINERをMakefile変数に割り当てる
# 未定義の場合はデフォルト値をfalseに設定
IN_CONTAINER ?= false

# コンテナ内から実行されたらRUN_CONTEXT変数を空で宣言し、それ以外はコンテナにアクセスする
ifeq ($(IN_CONTAINER), true)
	RUN_CONTEXT :=
else
	RUN_CONTEXT := docker compose exec app
endif

# 共通のコマンド実行関数を定義
define run-command
	$(RUN_CONTEXT) $(1)
endef

# 便利
ARG =
#################################################################################
# DOCKER-COMMAND                                                                #
#################################################################################
ps:
	docker compose ps

build:
	docker compose build $(ARG)

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

exec:
	docker compose exec app bash

logs:
	docker compose logs $(ARG)

build-prod:
	docker build --platform linux/amd64 -f Dockerfile.prod . -t $(ARG)

up-prod:
	docker run -itd --name rag_prod $(ARG)
	docker exec -it rag_prod bash

push:
	docker push $(ARG)

install:
	$(call run-command,poetry install)

own:
	$(call run-command,poetry install --only-root)

#################################################################################
# SCRIPT-COMMANDS                                                               #
#################################################################################
# どう使うかはちょっと検討
DEBUG =-m pdb

.PHONY: run
run:
	gunicorn -c ./gunicorn.conf.py 'main:serve()'

dev:
	$(call run-command,python main.py)

migrate-create:
	$(call run-command,alembic revision -m ${name})

migrate-auto:
	$(call run-command, alembic revision --autogenerate -m ${name})

migrate-up:
	$(call run-command,alembic upgrade head)

migrate-down:
	$(call run-command,alembic downgrade head)

migrate-history:
	$(call run-command,alembic history)

migrate-current:
	$(call run-command,alembic current)

test:
	$(call run-command,poetry run pytest -v ${arg})

fix: ruff-fix black

ruff-fix:
	$(call run-command,poetry run ruff --fix .)

black:
	$(call run-command,poetry run black .)

lint: black-check ruff-check mypy

ruff-check:
	$(call run-command,poetry run ruff check .)

black-check:
	$(call run-command,poetry run black --check .)

mypy:
	$(call run-command,poetry run mypy . --config-file ./pyproject.toml)
