import pytest
import re
import responses
from aioresponses import aioresponses, CallbackResult
import asyncio

from saucenao_api import SauceNao, AIOSauceNao
from saucenao_api.errors import (UnknownApiError, UnknownServerError, UnknownClientError, BadKeyError,
                                 BadFileSizeError, ShortLimitReachedError, LongLimitReachedError)
from . import test_suite as e

SAUCENAO_URL = SauceNao.SAUCENAO_URL
URL_PATTERN = re.compile(r'https://saucenao.com/search.php(.*)')


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mocked_aio_response():
    with aioresponses() as m:
        yield m


def test_from_url(mocked_responses):
    def request_callback(request):
        assert request.params['url'] == 'https://example.com/'
        return 500, {}, ''

    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    saucenao = SauceNao()
    with pytest.raises(UnknownApiError):
        saucenao.from_url('https://example.com/')


def test_async_from_url(mocked_aio_response):
    loop = asyncio.get_event_loop()

    def request_callback(url, **kwargs):
        assert kwargs['params']['url'] == 'https://example.com/'
        return CallbackResult(status=500, headers={}, body='')

    mocked_aio_response.post(URL_PATTERN, callback=request_callback)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(UnknownApiError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_from_file(mocked_responses):
    def request_callback(request):
        assert bin_file in request.body
        return 500, {}, ''

    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    with open('tests/test_suite.py', 'rb') as f:
        bin_file = f.read()
        f.seek(0)
        with pytest.raises(UnknownApiError):
            SauceNao().from_file(f)


def test_async_from_file(mocked_aio_response):
    loop = asyncio.get_event_loop()

    def request_callback(url, **kwargs):
        assert bin_file == kwargs['data']['file']
        return CallbackResult(status=500, headers={}, body='')

    mocked_aio_response.post(URL_PATTERN, callback=request_callback)

    with open('tests/test_suite.py', 'rb') as f:
        bin_file = f.read()
        f.seek(0)
        aio_saucenao = AIOSauceNao()
        with pytest.raises(UnknownApiError):
            loop.run_until_complete(aio_saucenao.from_file(bin_file))


def test_optional_params(mocked_responses):
    def request_callback(request):
        assert request.params['api_key'] == 'SauceNAO'
        assert request.params['dbmask'] == '12'
        assert request.params['dbmaski'] == '918'

        return 500, {}, ''

    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    saucenao = SauceNao('SauceNAO', dbmask=12, dbmaski=918)
    with pytest.raises(UnknownApiError):
        saucenao.from_url('https://example.com/')


def test_async_optional_params(mocked_aio_response):
    loop = asyncio.get_event_loop()

    def request_callback(url, **kwargs):
        assert kwargs['params']['api_key'] == 'SauceNAO'
        assert kwargs['params']['dbmask'] == 12
        assert kwargs['params']['dbmaski'] == 918

        return CallbackResult(status=500, headers={}, body='')

    mocked_aio_response.post(URL_PATTERN, callback=request_callback)

    aio_saucenao = AIOSauceNao('SauceNAO', dbmask=12, dbmaski=918)
    with pytest.raises(UnknownApiError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_403(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=403)
    with pytest.raises(BadKeyError):
        SauceNao().from_url('https://example.com/')


def test_async_403(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, status=403)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(BadKeyError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_413(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=413)
    with pytest.raises(BadFileSizeError):
        SauceNao().from_url('https://example.com/')


def test_async_413(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, status=413)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(BadFileSizeError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_429_short_limit_unregister(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=429, json=e.ShortLimitUnregister)
    with pytest.raises(ShortLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_async_429_short_limit_unregister(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, status=429, payload=e.ShortLimitUnregister)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(ShortLimitReachedError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_429_long_limit_unregister(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=429, json=e.LongLimitUnregister)
    with pytest.raises(LongLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_async_429_long_limit_unregister(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, status=429, payload=e.LongLimitUnregister)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(LongLimitReachedError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_status_below_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': -12}})
    with pytest.raises(UnknownClientError):
        SauceNao().from_url('https://example.com/')


def test_async_status_below_zero(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, payload={'header': {'user_id': '0', 'status': -12}})

    aio_saucenao = AIOSauceNao()
    with pytest.raises(UnknownClientError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_status_above_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': 12}})
    with pytest.raises(UnknownServerError):
        SauceNao().from_url('https://example.com/')


def test_async_status_above_zero(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, payload={'header': {'user_id': '0', 'status': 12}})

    aio_saucenao = AIOSauceNao()
    with pytest.raises(UnknownServerError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_user_id_below_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '-12', 'status': 0}})
    with pytest.raises(UnknownServerError):
        SauceNao().from_url('https://example.com/')


def test_async_user_id_below_zero(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, payload={'header': {'user_id': '-12', 'status': 0}})

    aio_saucenao = AIOSauceNao()
    with pytest.raises(UnknownServerError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_bad_api_key(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': 0}})
    with pytest.raises(BadKeyError):
        SauceNao('BadToken').from_url('https://example.com/')


def test_async_bad_api_key(mocked_aio_response):
    loop = asyncio.get_event_loop()

    mocked_aio_response.post(URL_PATTERN, payload={'header': {'user_id': '0', 'status': 0}})

    aio_saucenao = AIOSauceNao('BadToken')
    with pytest.raises(BadKeyError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_short_remaining_below_zero(mocked_responses):
    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': -1, 'long_remaining': 0}}
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=r)
    with pytest.raises(ShortLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_async_short_remaining_below_zero(mocked_aio_response):
    loop = asyncio.get_event_loop()

    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': -1, 'long_remaining': 0}}
    mocked_aio_response.post(URL_PATTERN, payload=r)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(ShortLimitReachedError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))


def test_long_remaining_below_zero(mocked_responses):
    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': 0, 'long_remaining': -1}}
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=r)
    with pytest.raises(LongLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_async_long_remaining_below_zero(mocked_aio_response):
    loop = asyncio.get_event_loop()

    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': 0, 'long_remaining': -1}}
    mocked_aio_response.post(URL_PATTERN, payload=r)

    aio_saucenao = AIOSauceNao()
    with pytest.raises(LongLimitReachedError):
        loop.run_until_complete(aio_saucenao.from_url('https://example.com/'))
