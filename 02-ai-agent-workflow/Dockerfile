FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root
COPY . .
EXPOSE 8001
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
