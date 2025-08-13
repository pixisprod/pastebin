FROM python:3.13-slim

RUN pip install --no-cache aiofiles==24.1.0
RUN pip install --no-cache https://github.com/pixisprod/pastebin-eventhub/archive/refs/heads/main.zip

WORKDIR /app

COPY src/ src/
COPY schemas/ schemas/

ENV PYTHONUNBUFFERED=1

CMD [ "python", "-m", "src.main" ]