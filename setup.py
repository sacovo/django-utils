from distutils.core import setup
setup(
    name='django-utils',
    version='1.3.2',
    author='Sandro Covo',
    author_email='sandro@covo.ch',
    packages=['djangoutils', 'djangoutils.views', 'djangoutils.templatetags'],
    description='django-utils is a python library to simplify the use of django.',
    install_requires=[
        'django',
    ],
)
