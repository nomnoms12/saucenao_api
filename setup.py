import setuptools


with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='saucenao_api',
    version='2.0.1',
    author='nomnoms12',
    author_email='alexander.ign0918@gmail.com',
    description='Wrapper for SauceNAO JSON API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nomnoms12/saucenao_api/',
    packages=['saucenao_api'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.6',
    install_requires=[
        'requests ~= 2.23.0',
    ],
    extras_require={
        'test': [
            'responses ~= 0.10.14',
            'pytest ~= 5.4.2',
            'pytest-cov ~= 2.8.1',
            'coveralls ~= 2.0.0',
        ],
    },
    project_urls={
       'Bug Reports': 'https://github.com/nomnoms12/saucenao_api/issues/',
       'Source': 'https://github.com/nomnoms12/saucenao_api/',
    },
)
