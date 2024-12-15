# App run
run:
  just _py python -Om src

# Up container
up:
  docker compose up --build


_py *args:
  uv run {{args}}
