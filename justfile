# App run
run:
  just _py python -Om src

# Install package with dependencies
install:
	uv sync --all-groups

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Up container
up:
  docker compose up --build


_py *args:
  uv run {{args}}
