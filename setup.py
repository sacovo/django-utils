from distutils.core import setup
setup(
    name='django-utils',
    version='1.0',
    author='Sandro Covo',
    author_email='sandro@covo.ch',
    packages=['djangoutils', 'djangoutils.views'],
    description='django-utils is a python library to simplify the use of django.',
    install_requires=[
        'django',
    ],
)
