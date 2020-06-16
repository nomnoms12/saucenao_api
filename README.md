![SauceNAO Logo](https://raw.githubusercontent.com/nomnoms12/saucenao_api/master/tests/logo.png)

# saucenao_api
[![Build Status](https://travis-ci.com/nomnoms12/saucenao_api.svg?branch=master)](https://travis-ci.com/nomnoms12/saucenao_api)
[![Coverage Status](https://coveralls.io/repos/github/nomnoms12/saucenao_api/badge.svg?branch=master)](https://coveralls.io/github/nomnoms12/saucenao_api?branch=master)
[![License](https://img.shields.io/github/license/nomnoms12/saucenao_api)](https://github.com/nomnoms12/saucenao_api/blob/master/LICENSE)
[![SauceNao Status](https://img.shields.io/website?url=https%3A%2F%2Fsaucenao.com)](https://saucenao.com)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saucenao_api)](https://pypi.org/project/saucenao-api)

> “The rough edges are a part of its charm”

Unofficial wrapper for the [SauceNAO](https://saucenao.com) JSON API

# Installation
This package requires Python 3.6 or later
```
pip install saucenao_api
```

## Dependencies
 - [requests](https://github.com/psf/requests)

# Usage
```python
from saucenao_api import SauceNao
from saucenao_api.params import DB, Hide, Bgcolor

# Parameters from https://saucenao.com/user.php?page=search-api
sauce = SauceNao(api_key=None,
                 testmode=0,
                 dbmask=None,
                 dbmaski=None,
                 db=DB.ALL,
                 numres=6,
                 hide=Hide.NONE,
                 bgcolor=Bgcolor.NONE)

# results = sauce.from_file(file)
results = sauce.from_url('https://i.imgur.com/oZjCxGo.jpg')

results.short_remaining  # 30 seconds limit
results.long_remaining   # 24 hours limit

len(results)  # 6
print(repr(results))
```
```python
<SauceResponse(results_count=6, long_remaining=99, short_remaining=3)>
```
The library provides common parameters, such as `similarity`, `title`, `url`, `author` and some others for almost all results:
```python
from saucenao_api import SauceNao

sauce = SauceNao()
results = sauce.from_url('https://i.imgur.com/oZjCxGo.jpg')

results[0].similarity  # 93.3
results[0].title       # めぐみん
results[0].url         # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77630170
results[0].author      # frgs
```
There are also special `VideoSauce` and `BookSauce` containers with extra parameters:
```python
from saucenao_api import SauceNao, VideoSauce, BookSauce

sauce = SauceNao()
result = sauce.from_url('https://i.imgur.com/k9xlw6f.jpg')[0]

if isinstance(result, VideoSauce):
    result.part      # 02
    result.year      # 2009-2009
    result.est_time  # 00:05:32 / 00:21:10

elif isinstance(result, BookSauce):
    result.part
```
# License
This package is based on [pysaucenao](https://github.com/FujiMakoto/pysaucenao).
