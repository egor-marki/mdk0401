import os
from pathlib import Path

from dotenv import load_dotenv

# корень проекта (две папки вверх)
BASE_DIR = Path(__file__).resolve().parent.parent

# читаем .env и кладём переменные в окружение
load_dotenv(BASE_DIR / ".env")

# ключ для подписи сессий и CSRF
SECRET_KEY = os.getenv("SECRET_KEY")
# True — режим разработки
DEBUG = os.getenv("DEBUG", "True") == "True"
# список разрешённых хостов
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# список подключённых приложений
INSTALLED_APPS = [
    "django.contrib.admin",        # встроенная админка
    "django.contrib.auth",         # встроенная авторизация
    "django.contrib.contenttypes", # типы контента (нужно для auth)
    "django.contrib.sessions",     # сессии
    "django.contrib.messages",     # всплывающие сообщения
    "django.contrib.staticfiles",   # статика (css/js)
]

# промежуточные слои между запросом и ответом
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", # сессии
    "django.middleware.common.CommonMiddleware",            # общие правила
    "django.middleware.csrf.CsrfViewMiddleware",            # защита от CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware", # request.user
    "django.contrib.messages.middleware.MessageMiddleware",  # messages framework
]

# где лежит корневой urls.py
ROOT_URLCONF = "config.urls"

# настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates", # движок Django
        "DIRS": [BASE_DIR / "templates"],                            # где искать общие шаблоны
        "APP_DIRS": True,                                             # искать также в templates/ приложений
        "OPTIONS": {
            "context_processors": [                                   # переменные во всех шаблонах
                "django.template.context_processors.request",         # request
                "django.contrib.auth.context_processors.auth",        # user
                "django.contrib.messages.context_processors.messages", # messages
            ],
        },
    },
]

# точка входа для сервера
WSGI_APPLICATION = "config.wsgi.application"

# настройки БД
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql", # драйвер PostgreSQL
        "NAME": os.getenv("POSTGRES_DB"),          # имя БД
        "USER": os.getenv("POSTGRES_USER"),        # пользователь
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),# пароль
        "HOST": os.getenv("POSTGRES_HOST"),        # хост
        "PORT": os.getenv("POSTGRES_PORT"),        # порт
    }
}

# кэш через Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache", # встроенный Redis-бэкенд
        "LOCATION": os.getenv("REDIS_URL"),                       # адрес Redis
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache" # сессии — в Redis
SESSION_CACHE_ALIAS = "default"                          # какой кэш использовать

# языковые настройки и локализация
LANGUAGE_CODE = "ru-ru"       # русский язык
TIME_ZONE = "Europe/Moscow"   # московское время
USE_I18N = True               # включить переводы
USE_TZ = True                 # хранить время с таймзоной

# настройки статических файлов
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"] # где искать статику

# настройки медиа-файлов
MEDIA_URL = "media/"                     # URL для загруженных файлов
MEDIA_ROOT = BASE_DIR / "media"          # папка для файлов

# тип ПК по умолчанию
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
