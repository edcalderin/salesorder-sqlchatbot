# Stage 1: Build
FROM python:3.12.9-slim AS builder

RUN pip install poetry==2.1.1

WORKDIR /sql_agent

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && poetry install --no-root --without dev

# Stage 2: Runtime
FROM python:3.12.9-slim

WORKDIR /sql_agent

COPY --from=builder /sql_agent .

ENV PATH="/sql_agent/.venv/bin:$PATH"

COPY sql_agent/ ./sql_agent

EXPOSE 8080

ENTRYPOINT [ "python", "-m", "streamlit", "run", "sql_agent/streamlit.py" ]