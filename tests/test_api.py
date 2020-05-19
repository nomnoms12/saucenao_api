import pytest
import responses

from saucenao_api import SauceNao
from saucenao_api.errors import (UnknownServerError, UnknownClientError, BadKeyError, BadFileSizeError,
                                 ShortLimitReachedError, LongLimitReachedError)
from . import examples as e


SAUCENAO_URL = SauceNao.SAUCENAO_URL


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_from_url(mocked_responses):
    def request_callback(request):
        assert request.params['url'] == 'https://example.com/'
        return 500, {}, ''
    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    saucenao = SauceNao()
    with pytest.raises(UnknownServerError):
        saucenao.from_url('https://example.com/')


def test_from_file(mocked_responses):
    def request_callback(request):
        assert bin_image in request.body
        return 500, {}, ''
    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    with open('tests/logo.png', 'rb') as f:
        bin_image = f.read()
        f.seek(0)
        with pytest.raises(UnknownServerError):
            SauceNao().from_file(f)


def test_optional_params(mocked_responses):
    def request_callback(request):
        print(request.params)
        assert request.params['api_key'] == 'SauceNAO'
        assert request.params['dbmask'] == '12'
        assert request.params['dbmaski'] == '918'

        return 500, {}, ''
    mocked_responses.add_callback(responses.POST, SAUCENAO_URL, callback=request_callback)

    saucenao = SauceNao('SauceNAO', dbmask=12, dbmaski=918)
    with pytest.raises(UnknownServerError):
        saucenao.from_url('https://example.com/')


def test_403(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=403)
    with pytest.raises(BadKeyError):
        SauceNao().from_url('https://example.com/')


def test_413(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=413)
    with pytest.raises(BadFileSizeError):
        SauceNao().from_url('https://example.com/')


def test_429_short_limit_unregister(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=429, json=e.ShortLimitUnregister)
    with pytest.raises(ShortLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_429_long_limit_unregister(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=429, json=e.LongLimitUnregister)
    with pytest.raises(LongLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_500(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, status=500)
    with pytest.raises(UnknownServerError):
        SauceNao().from_url('https://example.com/')


def test_status_below_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': -12}})
    with pytest.raises(UnknownClientError):
        SauceNao().from_url('https://example.com/')


def test_status_above_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': 12}})
    with pytest.raises(UnknownServerError):
        SauceNao().from_url('https://example.com/')


def test_user_id_below_zero(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '-12', 'status': 0}})
    with pytest.raises(UnknownServerError):
        SauceNao().from_url('https://example.com/')


def test_bad_api_key(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json={'header': {'user_id': '0', 'status': 0}})
    with pytest.raises(BadKeyError):
        SauceNao('BadToken').from_url('https://example.com/')


def test_short_remaining_below_zero(mocked_responses):
    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': -1, 'long_remaining': 0}}
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=r)
    with pytest.raises(ShortLimitReachedError):
        SauceNao().from_url('https://example.com/')


def test_long_remaining_below_zero(mocked_responses):
    r = {'header': {'user_id': '0', 'status': 0, 'short_remaining': 0, 'long_remaining': -1}}
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=r)
    with pytest.raises(LongLimitReachedError):
        SauceNao().from_url('https://example.com/')
