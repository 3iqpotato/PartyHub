# env_settings.py
# това ще е в гит хуб до края на изпита след това вече ще го премахна!!!
SECRET_KEY = 'django-insecure-+m)j&jexag@6thqwu$4#+0x)8^^6t8wt3)4^zyvksl2kl4kx8q'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PartyHub_db',
        'USER': 'postgres',
        'PASSWORD': 'kiko369963',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CSRF_TRUSTED_ORIGINS = ['https://a4d5-77-70-24-15.ngrok-free.app']


EMAIL_HOST_USER = 'kaloianralchev@gmail.com'  # Твоят имейл адрес
EMAIL_HOST_PASSWORD = 'gulz wswb sghj winm'  # Паролата за имейл акаунта
