# needed to make this a legit cool python package
# i have no idea what i'm doing

from setuptools import setup

setup(
    name='songscore',
    packages=['songscore'],
    include_package_data=True,
    install_requires=[
        'flask',
        'psycopg2',
        'urlparse'
    ],
)
