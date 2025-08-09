FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir https://github.com/pixisprod/pastebin-eventhub/archive/refs/heads/main.zip

COPY .env .
COPY src/ src/

ENV PYTHONUNBUFFERED=1

EXPOSE 8001

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001" ]