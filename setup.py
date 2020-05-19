import setuptools


with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='saucenao_api',
    version='0.1',
    author='nomnoms12',
    author_email='alexander.ign0918@gmail.com',
    description='Unofficial wrapper for SauceNAO JSON API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nomnoms12/saucenao_api',
    packages=setuptools.find_packages('saucenao_api'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6, <4',
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
       'Bug Reports': 'https://github.com/nomnoms12/saucenao_api/issues',
       'Source': 'https://github.com/nomnoms12/saucenao_api/',
    },
)
