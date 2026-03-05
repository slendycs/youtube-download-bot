## Пример `docker-compose.yml`

```yml
services:
  yt-bot:
    image: ghcr.io/slendycs/youtube-download-bot:latest
    container_name: bot_container
    user: "<username>:<groupname>"
    networks:
      - bot-network
    environment:
      - BOT_TOKEN=<Telegram-API bot token>
      - LOG_LEVEL=<debug/info/warning/error/critical>
      - REDIS_PASSWORD=<redis password>
      - REDIS_HOST=redis
      - REDIS_PORT=<redis port>
    volumes:
      - <path to downloads>:/app/downloads
    depends_on:
      - redis

  redis:
    image: redis:latest
    container_name: redis_container
    networks:
      - bot-network
    environment:
      REDIS_PASSWORD: <redis password>
    volumes:
      - redis-data:/data
    command: >
      sh -c 'redis-server --requirepass <redis password> --appendonly yes'
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "<redis password>", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

volumes:
  redis-data:

networks:
  bot-network:
```