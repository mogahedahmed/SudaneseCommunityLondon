import os
import mimetypes
from pathlib import Path

# تعريف BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان (غيّره قبل النشر الحقيقي)
SECRET_KEY = 'django-insecure-your-secret-key'

# Debug و Hosts
DEBUG = True
ALLOWED_HOSTS = ['sudanesecommunitylondon.pythonanywhere.com', 'www.sudanesecommunitylondon.pythonanywhere.com']



# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # التطبيقات الخاصة بك
    'main',
    'news',
    'contact',
    'activities',
    'regulations',
    'vote.apps.VoteConfig',

]

# الوسطاء Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لدعم static في Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware لتسجيل خروج المستخدم عند إغلاق المتصفح
    'vote.middleware.LogoutOnBrowserCloseMiddleware',
]

ROOT_URLCONF = 'SudaneseCommunity.urls'

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'main', 'templates'),
            os.path.join(BASE_DIR, 'vote', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SudaneseCommunity.wsgi.application'

# إعدادات قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# إعدادات التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والوقت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_TZ = True

# إعدادات static
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'main', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# إعدادات media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# إصلاح مشاكل تحميل ملفات js في بعض السيرفرات
mimetypes.add_type("application/javascript", ".js", True)

# Whitenoise لتجهيز ملفات static عند النشر
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# القيمة الافتراضية لحقل ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 دقيقة
