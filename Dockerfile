FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn pydantic openai python-dotenv httpx openenv-core

COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "-m", "server.app"]
