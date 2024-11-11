path := .

define Comment
	- Run `make help` to see all the available options.
	- Run `make lint` to run the linter.
	- Run `make lint-check` to check linter conformity.
	- Run `dep-lock` to lock the deps in 'requirements.txt' and 'requirements-dev.txt'.
	- Run `dep-sync` to sync current environment up to date with the locked deps.
endef


.PHONY: lint
lint: ruff mypy	## Apply all the linters.

.PHONY: lint-check
lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@uv run ruff check $(path)
	@uv run mypy $(path)

.PHONY: ruff
ruff: ## Apply ruff.
	@echo "Applying ruff..."
	@echo "================"
	@echo
	@uv run ruff check --fix $(path)
	@uv run ruff format $(path)

.PHONY: mypy
mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@uv run mypy $(path)

.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run the tests against the current version of Python.
	cd app && uv run pytest -vv && cd ..

.PHONY: dep-lock
dep-lock: ## Freeze deps in 'requirements*.txt' files.
	@uv lock


.PHONY: dep-sync
dep-sync: ## Sync venv installation with 'requirements.txt' file.
	@uv sync

.PHONY: run-container
run-container: ## Run the app in a docker container.
	docker compose up --build -d

.PHONY: kill-container
kill-container: ## Stop the running docker container.
	docker compose down

.PHONY: run-local
run-local: ## Run the app locally.
	uv run uvicorn app.main:app --port 5002 --reload

.PHONY: run-local-bakery
run-local-bakery: ## Run the bakery service locally.
	uv run python bakery_grpc/main.py

.PHONY: run-local-celery
run-local-celery: ## Run the celery service locally.
	celery -A app.core.celery.celery worker --loglevel=debug

proto:
	uv run python -m grpc_tools.protoc -I./bakery_grpc/protos --python_out=./bakery_grpc/ --pyi_out=./bakery_grpc --grpc_python_out=./bakery_grpc/ ./bakery_grpc/protos/bakery.proto