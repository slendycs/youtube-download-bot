FROM python:3.13.3-slim

ARG APP_USER=apps
ARG APP_UID=568
ARG APP_GID=568

# Создание пользователя
RUN groupadd -g ${APP_GID} ${APP_USER} && \
    useradd -u ${APP_UID} -g ${APP_GID} -m ${APP_USER}

# Системные зависимости
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код приложения
COPY src/ /app/src
RUN chown -R ${APP_USER}:${APP_USER} /app/src && \
    chmod -R 755 /app/src

# Папка для данных
RUN mkdir -p /app/downloads && \
    chmod 777 /app/downloads

# Переключение пользователя
USER ${APP_USER}

# Запуск приложения
WORKDIR /app/src
CMD ["python", "-m", "main.main"]