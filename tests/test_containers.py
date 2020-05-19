import pytest
import responses

from saucenao_api import SauceNao
from saucenao_api.containers import BasicSauce, BookSauce, VideoSauce
from . import examples as e


SAUCENAO_URL = SauceNao.SAUCENAO_URL


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_response_attrs(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    assert results.raw == e.HMagazines
    assert results.user_id == e.HMagazines['header']['user_id']
    assert results.account_type == e.HMagazines['header']['account_type']
    assert results.short_limit == e.HMagazines['header']['short_limit']
    assert results.long_limit == e.HMagazines['header']['long_limit']
    assert results.long_remaining == e.HMagazines['header']['long_remaining']
    assert results.short_remaining == e.HMagazines['header']['short_remaining']
    assert results.status == e.HMagazines['header']['status']
    assert results.results_requested == e.HMagazines['header']['results_requested']
    assert results.search_depth == e.HMagazines['header']['search_depth']
    assert results.minimum_similarity == e.HMagazines['header']['minimum_similarity']
    assert results.query_image_display == e.HMagazines['header']['query_image_display']
    assert results.query_image == e.HMagazines['header']['query_image']
    assert results.results_returned == e.HMagazines['header']['results_returned']


def test_response_len(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    assert len(results) == len(e.HMagazines['results'])


def test_response_repr(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    r = (f'<SauceResponse(results_count={len(results)}, long_remaining={results.long_remaining}, '
         f'short_remaining={results.short_remaining})>')
    assert repr(results) == r


def test_empty_results(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.DoujinshiDB)
    results = SauceNao().from_url('https://example.com/')

    assert results.results == []


def test_basic_attrs(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.raw == e.HMagazines['results'][0]
    assert result.similarity == float(e.HMagazines['results'][0]['header']['similarity'])
    assert result.thumbnail == e.HMagazines['results'][0]['header']['thumbnail']
    assert result.index_id == e.HMagazines['results'][0]['header']['index_id']
    assert result.index_name == e.HMagazines['results'][0]['header']['index_name']


def test_hmagazines(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.HMagazines['results'][0]['data']['title']
    assert result.url is None
    assert result.author is None
    assert type(result) is BookSauce
    assert result.part == e.HMagazines['results'][0]['data']['part']


def test_hgamecg(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HGame_CG)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.HGame_CG['results'][0]['data']['title']
    assert result.url == f'http://www.getchu.com/soft.phtml?id={e.HGame_CG["results"][0]["data"]["getchu_id"]}'
    assert result.author == e.HGame_CG['results'][0]['data']['company']
    assert type(result) is BasicSauce


def test_pixivimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Pixiv_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Pixiv_Images['results'][0]['data']['title']
    assert result.url == e.Pixiv_Images['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Pixiv_Images['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_niconicoseiga(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Nico_Nico_Seiga)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Nico_Nico_Seiga['results'][0]['data']['title']
    assert result.url == e.Nico_Nico_Seiga['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Nico_Nico_Seiga['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_danbooru(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Danbooru)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Danbooru['results'][0]['data']['material']
    assert result.url == e.Danbooru['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Danbooru['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_drawrimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Drawr_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Drawr_Images['results'][0]['data']['title']
    assert result.url == e.Drawr_Images['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Drawr_Images['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_nijieimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Nijie_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Nijie_Images['results'][0]['data']['title']
    assert result.url == e.Nijie_Images['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Nijie_Images['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_yandere(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Yandere)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Yandere['results'][0]['data']['material']
    assert result.url == e.Yandere['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Yandere['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_fakku(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.FAKKU)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.FAKKU['results'][0]['data']['source']
    assert result.url == e.FAKKU['results'][0]['data']['ext_urls'][0]
    assert result.author == e.FAKKU['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_hmisc(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMisc)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.HMisc['results'][0]['data']['eng_name']
    assert result.url is None
    assert result.author == e.HMisc['results'][0]['data']['creator'][0]
    assert type(result) is BasicSauce


def test_twodmarket(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.TwoDMarket)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.TwoDMarket['results'][0]['data']['source']
    assert result.url == e.TwoDMarket['results'][0]['data']['ext_urls'][0]
    assert result.author == e.TwoDMarket['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_medibang(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.MediBang)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.MediBang['results'][0]['data']['title']
    assert result.url == e.MediBang['results'][0]['data']['ext_urls'][0]
    assert result.author == e.MediBang['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_anime(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Anime)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Anime['results'][0]['data']['source']
    assert result.url == e.Anime['results'][0]['data']['ext_urls'][0]
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == e.Anime['results'][0]['data']['part']
    assert result.year == e.Anime['results'][0]['data']['year']
    assert result.est_time == e.Anime['results'][0]['data']['est_time']


def test_hanime(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HAnime)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.HAnime['results'][0]['data']['source']
    assert result.url == e.HAnime['results'][0]['data']['ext_urls'][0]
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == e.HAnime['results'][0]['data']['part']
    assert result.year == e.HAnime['results'][0]['data']['year']
    assert result.est_time == e.HAnime['results'][0]['data']['est_time']


def test_movies(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Movies)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Movies['results'][0]['data']['source']
    assert result.url == e.Movies['results'][0]['data']['ext_urls'][0]
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == e.Movies['results'][0]['data']['part']
    assert result.year == e.Movies['results'][0]['data']['year']
    assert result.est_time == e.Movies['results'][0]['data']['est_time']


def test_shows(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Shows)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Shows['results'][0]['data']['source']
    assert result.url == e.Shows['results'][0]['data']['ext_urls'][0]
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == e.Shows['results'][0]['data']['part']
    assert result.year == e.Shows['results'][0]['data']['year']
    assert result.est_time == e.Shows['results'][0]['data']['est_time']


def test_gelbooru(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Gelbooru)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Gelbooru['results'][0]['data']['material']
    assert result.url == e.Gelbooru['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Gelbooru['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_konachan(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Konachan)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Konachan['results'][0]['data']['material']
    assert result.url == e.Konachan['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Konachan['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_sankakuchannel(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.SankakuChannel)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.SankakuChannel['results'][0]['data']['material']
    assert result.url == e.SankakuChannel['results'][0]['data']['ext_urls'][0]
    assert result.author == e.SankakuChannel['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_e621net(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.E621net)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.E621net['results'][0]['data']['material']
    assert result.url == e.E621net['results'][0]['data']['ext_urls'][0]
    assert result.author == e.E621net['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_idolcomplex(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.IdolComplex)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.IdolComplex['results'][0]['data']['material']
    assert result.url == e.IdolComplex['results'][0]['data']['ext_urls'][0]
    assert result.author == e.IdolComplex['results'][0]['data']['creator']
    assert type(result) is BasicSauce


def test_bcynetillust(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Bcynet_Illust)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Bcynet_Illust['results'][0]['data']['title']
    assert result.url == e.Bcynet_Illust['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Bcynet_Illust['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_bcynetcosplay(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Bcynet_Cosplay)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Bcynet_Cosplay['results'][0]['data']['title']
    assert result.url == e.Bcynet_Cosplay['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Bcynet_Cosplay['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_portalgraphicsnet(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.PortalGraphicsnet)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.PortalGraphicsnet['results'][0]['data']['title']
    assert result.url == e.PortalGraphicsnet['results'][0]['data']['ext_urls'][0]
    assert result.author == e.PortalGraphicsnet['results'][0]['data']['member_name']
    assert type(result) is BasicSauce


def test_deviantart(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.DeviantArt)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.DeviantArt['results'][0]['data']['title']
    assert result.url == e.DeviantArt['results'][0]['data']['ext_urls'][0]
    assert result.author == e.DeviantArt['results'][0]['data']['author_name']
    assert type(result) is BasicSauce


def test_pawoonet(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Pawoonet)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Pawoonet['results'][0]['data']['created_at']
    assert result.url == e.Pawoonet['results'][0]['data']['ext_urls'][0]
    assert result.author == e.Pawoonet['results'][0]['data']['pawoo_user_username']
    assert type(result) is BasicSauce


def test_madokami(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Madokami)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.Madokami['results'][0]['data']['source']
    assert result.url == e.Madokami['results'][0]['data']['ext_urls'][0]
    assert result.author is None
    assert type(result) is BookSauce
    assert result.part == e.Madokami['results'][0]['data']['part']


def test_mangadex(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.MangaDex)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == e.MangaDex['results'][0]['data']['source']
    assert result.url == e.MangaDex['results'][0]['data']['ext_urls'][0]
    assert result.author == e.MangaDex['results'][0]['data']['author']
    assert type(result) is BookSauce
    assert result.part == e.MangaDex['results'][0]['data']['part']
