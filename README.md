# 📥 YouTube Download Bot

Telegram-бот для удобного скачивания видео и аудио с YouTube. Поддерживает загрузку как отдельных потоков, так и их последующую автоматическую склейку (видео + аудио), предоставляя интуитивный интерфейс через инлайн-кнопки и уведомления о статусе выполнения.

## ✨ Возможности

- 📥 Скачивание видео и аудио с YouTube по ссылке или ID.
- 🔗 Автоматическая склейка видео и аудио дорожек в один файл (через `moviepy`).
- ⚡ Полностью асинхронная работа благодаря `aiogram`
- 📦 Готовая поддержка Docker и `docker-compose`.
- 🔄 Интеграция с Redis для надежного управления состояниями и очередями задач.
- 📝 Информативные сообщения о начале и завершении процесса загрузки.

## 🛠 Стек технологий

- **Python 3.9**
- **[aiogram](https://github.com/aiogram/aiogram)** – фреймворк для Telegram Bot API
- **[pytubefix](https://github.com/JuanBindez/pytubefix)** – надежная загрузка контента с YouTube
- **[moviepy](https://github.com/Zulko/moviepy)** – обработка и склейка медиафайлов
- **redis** – хранение состояний и кэширование
- **python-decouple** – безопасное управление переменными окружения
- **Docker & GitHub Actions** – контейнеризация и автоматический CI/CD

## ⚙️ Установка и запуск

### Вариант 1: Docker (Рекомендуемый) 🐳

Самый простой, чистый и надежный способ запуска, изолирующий зависимости.

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/slendycs/youtube-download-bot.git
   cd youtube-download-bot
   ```
2. Создайте файл `.env` на основе примера:
   ```bash
   cp env.example .env
   ```
3. Отредактируйте `.env`, указав ваши данные (токен бота, пароль Redis и т.д.).
4. Откройте `docker-compose.yml` и замените `<username>:<groupname>` на вашего пользователя и группу (например, `1000:1000`). Это критически важно для избежания проблем с правами доступа при записи файлов в папку `downloads`.
5. Запустите контейнеры:
   ```bash
   docker compose up -d
   ```

### Вариант 2: Локальный запуск 💻

1. Убедитесь, что у вас установлены **Python 3.9+**, **FFmpeg** (для moviepy) и запущен **Redis**.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/slendycs/youtube-download-bot.git
   cd youtube-download-bot
   ```
3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
6. Создайте файл `.env` (см. раздел "Конфигурация") и запустите бота:
   ```bash
   python -m src.main  # Укажите правильный путь к вашему главному файлу запуска
   ```

## 📝 Конфигурация

Создайте файл `.env` в корне проекта и заполните его следующими параметрами:
```env
# Токен вашего Telegram-бота от @BotFather
BOT_TOKEN=your_telegram_bot_token_here

# Уровень логирования: debug, info, warning, error, critical
LOG_LEVEL=info

# Настройки Redis
REDIS_PASSWORD=your_secure_redis_password
REDIS_HOST=localhost  # Используйте 'redis', если запускаете через docker-compose
REDIS_PORT=6379
```

## 🚀 Использование

1. Запустите бота и отправьте ему ссылку на видео YouTube или его ID.
2. Выберите желаемый формат загрузки с помощью появившихся инлайн-кнопок.
3. Бот отправит уведомление о начале обработки.
4. После завершения (и склейки, если требуется) вы получите готовый файл прямо в чат.

## 🔄 CI/CD и Docker-образы

Проект настроен на автоматическую сборку Docker-образа через GitHub Actions при обновлении кода.
Последний стабильный образ доступен в GitHub Container Registry:
```bash
docker pull ghcr.io/slendycs/youtube-download-bot:latest
```
