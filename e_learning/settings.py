
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = "django-insecure-(&$hn2%o(&d(f!o$$3b-=*&g+y=mtldom_lsgtp1^r@gm!$&t7"


DEBUG = True

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    "courses.apps.CoursesConfig",
    'corsheaders', 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "e_learning.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "e_learning.wsgi.application"




DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]




LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



STATIC_URL = "static/"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'




SESSION_COOKIE_AGE = 30 * 24 * 60 * 60  



CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

