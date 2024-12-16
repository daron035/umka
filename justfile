# App run
run:
  just _py python -Om src

# Install package with dependencies
install:
	uv sync --all-groups

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Run tests
test *args:
  just _py pytest {{args}}

# Up api container
api:
  docker compose --profile api up --build -d

# Up postgres container
pg:
  docker compose --profile postgres_db up --build -d

# Up entire project
up:
  docker compose --profile api \
    --profile postgres_db up --build -d


_py *args:
  uv run {{args}}
