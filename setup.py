from setuptools import setup

setup(
    name='songscore',
    packages=['songscore'],
    include_package_data=True,
    install_requires=[
        'flask',
        'wtforms',
        'passlib',
        'psycopg2-binary'
    ],
 )
