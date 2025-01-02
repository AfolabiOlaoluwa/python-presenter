from django.conf import settings

pytest_plugins = ['pytest_django']


def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=['python_presenter'],
        SECRET_KEY='django-insecure-t3st-k3y-8675309-n0t-4-pr0duct10n-&x#42',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'DIR': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'libraries': {
                    'presenter_tag': 'python_presenter.core.templatetags.presenter_tag',
                },
            },
        }],
    )
