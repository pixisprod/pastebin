FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir https://github.com/pixisprod/pastebin-eventhub/archive/refs/heads/main.zip

COPY src/ src/

EXPOSE 8002

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]