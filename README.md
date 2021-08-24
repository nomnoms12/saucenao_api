![SauceNAO Logo](https://user-images.githubusercontent.com/44947427/89287471-b9289000-d65c-11ea-905d-aa72f908a9b3.png)

# saucenao_api
[![Tests](https://github.com/nomnoms12/saucenao_api/workflows/Tests/badge.svg?branch=master)](https://github.com/nomnoms12/saucenao_api/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/nomnoms12/saucenao_api/branch/master/graph/badge.svg)](https://codecov.io/gh/nomnoms12/saucenao_api)
[![License](https://img.shields.io/github/license/nomnoms12/saucenao_api)](https://github.com/nomnoms12/saucenao_api/blob/master/LICENSE)
[![SauceNao Status](https://img.shields.io/website?url=https%3A%2F%2Fsaucenao.com)](https://saucenao.com)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saucenao_api)](https://pypi.org/project/saucenao-api)

> “The rough edges are a part of its charm”

Unofficial wrapper for the [SauceNAO](https://saucenao.com) JSON API

# Installation
This package requires Python 3.6 or later.
```
pip install -U saucenao_api
```

# Usage
```python
from saucenao_api import SauceNao

# Replace the key with your own
sauce = SauceNao('077f16b38a2452401790540f41246c7d951330c0')
results = sauce.from_url('https://i.imgur.com/oZjCxGo.jpg')  # or from_file()

best = results[0]  # results sorted by similarity
```

The library attempts to provide a developer friendly container format for all results. Meaning, no matter if SauceNao returns a Pixiv source result or a more obscure source, you'll be able to easily pull the `title`, `urls`, `author` and other useful information:
```python
from saucenao_api import SauceNao
results = SauceNao('077f16b38a2452401790540f41246c7d951330c0').from_url('https://i.imgur.com/oZjCxGo.jpg')

len(results)   # 6
bool(results)  # True

# Request limits
results.short_remaining  # 4  (per 30 seconds limit)
results.long_remaining   # 99 (per day limit)

results[0].thumbnail     # temporary URL for picture preview
results[0].similarity    # 93.3
results[0].title         # めぐみん
results[0].urls          # ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77630170']
results[0].author        # frgs
results[0].raw           # raw result
```

Video search results and book search results provide additional attributes:
```python
from saucenao_api import SauceNao, VideoSauce, BookSauce
result = SauceNao('077f16b38a2452401790540f41246c7d951330c0').from_url('https://i.imgur.com/k9xlw6f.jpg')[0]

if isinstance(result, VideoSauce):
    result.part      # 02
    result.year      # 2009-2009
    result.est_time  # 00:05:32 / 00:21:10

elif isinstance(result, BookSauce):
    result.part
```
*You can use the `dir` function to see all the attributes.*

## Asyncio
```python
import asyncio
from saucenao_api import AIOSauceNao

async def main():
    # async requesting is also supported via the AIOSauceNao class
    async with AIOSauceNao('077f16b38a2452401790540f41246c7d951330c0') as aio:
        results = await aio.from_url('https://i.imgur.com/k9xlw6f.jpg')
    
asyncio.run(main())
```
The async with functionality is pretty useful if you want to make multiple requests.
Note that you can still search without the `async with` syntax by simply calling `await AIOSauceNao(...).from_url(...)`.

## Advanced usage
```python
from saucenao_api import SauceNao
from saucenao_api.params import DB, Hide, BgColor

sauce = SauceNao(api_key=None,          # Optional[str] 
                 testmode=0,            # int
                 dbmask=None,           # Optional[int]
                 dbmaski=None,          # Optional[int]
                 db=DB.ALL,             # int
                 numres=6,              # int
                 frame=1,               # int
                 hide=Hide.NONE,        # int
                 bgcolor=BgColor.NONE,  # int
)
```
The parameters `frame`, `hide` and `bgcolor` are taken from the main page and from the [testing page](https://saucenao.com/testing), so their performance is not guaranteed. For the rest see [SauceNAO User Config](https://saucenao.com/user.php?page=search-api) page (registration required).

### Exceptions
All exceptions inherit from `SauceNaoApiError` for easy catching and handling. See [`errors.py`](saucenao_api/errors.py) file for details.

*Note: SauceNao doesn't have good documentation. Exceptions are created only based on observations of changes in the returned status codes. If you find a specific error that is not being processed, please report it.*

# License
This package is based on [`pysaucenao`](https://github.com/FujiMakoto/pysaucenao).
