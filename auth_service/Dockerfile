FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
RUN pip install https://github.com/pixisprod/pastebin-schemas-lib/archive/refs/heads/main.zip

COPY .env .
COPY src/ src/

EXPOSE 8000

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001" ]