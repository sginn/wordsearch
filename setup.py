from setuptools import setup

setup(
    name='wordsearch',
    version='0.0',
    entry_points={
        'console_scripts': [
            'wordsearch=wordsearch.main:main',
        ],
    },
)
