from setuptools import setup

setup(
    name='Songscore API',
    packages=['songscore_api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'psycopg2-binary',
        'flask-httpauth',
        'passlib'
    ],
 )
