FROM python:3.13-slim

RUN pip install aiofiles==24.1.0
RUN pip install https://github.com/pixisprod/pastebin-eventhub/archive/refs/heads/main.zip

WORKDIR /app

COPY src/ src/
COPY schemas/ schemas/


CMD [ "python", "-m", "src.main" ]