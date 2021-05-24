import pytest
import responses

from saucenao_api import SauceNao
from saucenao_api.containers import BasicSauce, BookSauce, VideoSauce
from . import test_suite as e


SAUCENAO_URL = SauceNao.SAUCENAO_URL


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_response_attrs(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    assert results.raw == e.HMagazines
    assert results.user_id == 0
    assert results.account_type == 0
    assert results.short_limit == '4'
    assert results.long_limit == '100'
    assert results.long_remaining == 65
    assert results.short_remaining == 1
    assert results.status == 0
    assert results.results_requested == 6
    assert results.search_depth == '128'
    assert results.minimum_similarity == -3.04
    assert results.results_returned == 5


def test_response_len(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    assert len(results) == 5


def test_response_bool(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    results = SauceNao().from_url('https://example.com/')

    assert bool(results) is True

    mocked_responses.remove(responses.POST, SAUCENAO_URL)
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.DoujinshiDB)
    results = SauceNao().from_url('https://example.com/')

    assert bool(results) is False


def test_response_repr(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HGame_CG)
    results = SauceNao().from_url('https://example.com/')

    assert repr(results) == '<SauceResponse(count=5, long_remaining=66, short_remaining=1)>'
    assert repr(results[0]) == "<BasicSauce(title='Haramiko', similarity=17.47)>"

    mocked_responses.remove(responses.POST, SAUCENAO_URL)
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    result = SauceNao().from_url('https://example.com/')[0]

    assert repr(result) == "<BookSauce(title='Hime Dorobou', part='[2001-01]', similarity=0.37)>"

    mocked_responses.remove(responses.POST, SAUCENAO_URL)
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Anime)
    result = SauceNao().from_url('https://example.com/')[0]

    assert repr(result) == "<VideoSauce(title='One Piece', part='299', similarity=19.50)>"


def test_empty_results(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.DoujinshiDB)
    results = SauceNao().from_url('https://example.com/')

    assert results.results == []


def test_basic_attrs(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.raw == {'header': {'similarity': '0.37', 'thumbnail': 'https://img1.saucenao.com/res/0_magazines/Hime%20Dorobou/%5B2001-01%5D/051.JPG?auth=oH21gSB37fnx04zMNaMVvg&exp=1596483537', 'index_id': 0, 'index_name': 'Index #0: H-Magazines - 051.JPG'}, 'data': {'title': 'Hime Dorobou', 'part': '[2001-01]', 'date': '2001-01'}}, {'header': {'similarity': '0.0638999999999', 'thumbnail': 'https://img1.saucenao.com/res/0_magazines/Slave%20Heroines/10%20%5B2009-01%5D/001.jpg?auth=IWwXAQXqZk4ZgkjiZ7C1Xg&exp=1596483537', 'index_id': 0, 'index_name': 'Index #0: H-Magazines - 001.jpg'}, 'data': {'title': 'Slave Heroines', 'part': 'vol. 10', 'date': '2009-01'}}
    assert result.similarity == 0.37
    assert result.thumbnail == 'https://img1.saucenao.com/res/0_magazines/Hime%20Dorobou/%5B2001-01%5D/051.JPG?auth=oH21gSB37fnx04zMNaMVvg&exp=1596483537'
    assert result.index_id == 0
    assert result.index_name == 'Index #0: H-Magazines - 051.JPG'


def test_hmagazines(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMagazines)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Hime Dorobou'
    assert result.urls == []
    assert result.author is None
    assert type(result) is BookSauce
    assert result.part == '[2001-01]'


def test_hgamecg(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HGame_CG)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Haramiko'
    assert result.urls == ['http://www.getchu.com/soft.phtml?id=587705']
    assert result.author == 'Selen'
    assert type(result) is BasicSauce


def test_pixivimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Pixiv_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '妖キャラをカリスマ化してみた。'
    assert result.urls == ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=4933944']
    assert result.author == '佳虫'
    assert type(result) is BasicSauce


def test_niconicoseiga(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Nico_Nico_Seiga)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'ボイスロイドたちの学園クトゥルフ'
    assert result.urls == ['https://seiga.nicovideo.jp/seiga/im3917445']
    assert result.author == 'ナギネコ'
    assert type(result) is BasicSauce


def test_danbooru(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Danbooru)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'highly responsive to prayers, touhou, touhou (pc-98)'
    assert result.urls == ['https://danbooru.donmai.us/post/show/736634']
    assert result.author == 'nichimatsu seri'
    assert type(result) is BasicSauce


def test_drawrimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Drawr_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '2012-05-07 03:41:38'
    assert result.urls == ['https://drawr.net/show.php?id=3728320']
    assert result.author == 'CAMfc'
    assert type(result) is BasicSauce


def test_nijieimages(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Nijie_Images)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Broadcasting accident - All Five !!'
    assert result.urls == ['https://nijie.info/view.php?id=334086']
    assert result.author == '青虫'
    assert type(result) is BasicSauce


def test_yandere(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Yandere)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'metal gear'
    assert result.urls == ['https://yande.re/post/show/33539']
    assert result.author == ''
    assert type(result) is BasicSauce


def test_fakku(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.FAKKU)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Ima Real'
    assert result.urls == ['https://www.fakku.net/hentai/ima-real-english']
    assert result.author == 'Takeda Hiromitsu'
    assert type(result) is BasicSauce


def test_hmisc(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMisc)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '[Erect Sawaru] Shinkyoku no Grimoire III -PANDRA saga 2nd story-'
    assert result.urls == []
    assert result.author == 'erect sawaru | moroboshi guy'
    assert type(result) is BasicSauce


def test_twodmarket(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.TwoDMarket)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Rain Shelter Tale'
    assert result.urls == ['https://2d-market.com/Comic/133']
    assert result.author == 'Kabayakiya'
    assert type(result) is BasicSauce


def test_medibang(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.MediBang)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '戦闘摂理解析システム'
    assert result.urls == ['https://medibang.com/picture/gu1802142236123490002513827']
    assert result.author == '紅羽'
    assert type(result) is BasicSauce


def test_anime(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Anime)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'One Piece'
    assert result.urls == ['https://anidb.net/anime/69']
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == '299'
    assert result.year == '1999'
    assert result.est_time == '00:12:59 / 00:23:20'


def test_hanime(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HAnime)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Onmyouji Ayakashi no Megami: Inran Jubaku'
    assert result.urls == ['https://anidb.net/anime/7065']
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == '1'
    assert result.year == '2009-2010'
    assert result.est_time == '00:02:18 / 00:28:24'


def test_movies(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Movies)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Tombstone'
    assert result.urls == ['https://www.imdb.com/title/tt0108358']
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part is None
    assert result.year == '1993'
    assert result.est_time == '01:10:44 / 02:09:38'


def test_shows(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Shows)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Star Trek - Enterprise'
    assert result.urls == ['https://www.imdb.com/title/tt0244365']
    assert result.author is None
    assert type(result) is VideoSauce
    assert result.part == 'S01E21'
    assert result.year == '2001-2005'
    assert result.est_time == '00:02:53 / 00:44:24'


def test_gelbooru(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Gelbooru)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'atlus, persona, persona 4'
    assert result.urls == ['https://gelbooru.com/index.php?page=post&s=view&id=559170']
    assert result.author == 'chinchikooru (pixiv)'
    assert type(result) is BasicSauce


def test_konachan(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Konachan)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'tengen toppa gurren lagann'
    assert result.urls == ['https://konachan.com/post/show/82192']
    assert result.author == 'gainax, nanao'
    assert type(result) is BasicSauce


def test_sankakuchannel(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.SankakuChannel)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'harry potter'
    assert result.urls == ['https://chan.sankakucomplex.com/post/show/4922724']
    assert result.author == ''
    assert type(result) is BasicSauce


def test_e621net(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.E621net)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == ''
    assert result.urls == ['https://e621.net/post/show/1410034']
    assert result.author == 'unknown artist'
    assert type(result) is BasicSauce


def test_idolcomplex(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.IdolComplex)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == ''
    assert result.urls == ['https://idol.sankakucomplex.com/post/show/441604']
    assert result.author == ''
    assert type(result) is BasicSauce


def test_bcynetillust(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Bcynet_Illust)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '|*美食方言*|'
    assert result.urls == ['https://bcy.net/illust/detail/55206']
    assert result.author == '第四存档点'
    assert type(result) is BasicSauce


def test_bcynetcosplay(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Bcynet_Cosplay)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '2015總結 星名皇'
    assert result.urls == ['https://bcy.net/coser/detail/54748']
    assert result.author == '星名皇'
    assert type(result) is BasicSauce


def test_portalgraphicsnet(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.PortalGraphicsnet)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '並べた'
    assert result.urls == ['https://web.archive.org/web/http://www.portalgraphics.net/pg/illust/?image_id=77837']
    assert result.author == '神崎'
    assert type(result) is BasicSauce


def test_deviantart(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.DeviantArt)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Koshitantan + video link+stagedl'
    assert result.urls == ['https://deviantart.com/view/515715132']
    assert result.author == 'SliverRose0916'
    assert type(result) is BasicSauce


def test_pawoonet(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Pawoonet)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '2017-10-11T12:29:20.000Z'
    assert result.urls == ['https://pawoo.net/@nez_ebi']
    assert result.author == 'nez_ebi'
    assert type(result) is BasicSauce


def test_madokami(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Madokami)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Maou Dante'
    assert result.urls == ['https://www.mangaupdates.com/series.html?id=4451']
    assert result.author is None
    assert type(result) is BookSauce
    assert result.part == 'Maou Dante v01'


def test_mangadex(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.MangaDex)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Prison School'
    assert result.urls == ['https://mangadex.org/chapter/53801/',
                          'https://www.mangaupdates.com/series.html?id=63043',
                          'https://myanimelist.net/manga/25297/']
    assert result.author == 'Hiramoto Akira'
    assert type(result) is BookSauce
    assert result.part == ' - Chapter 27'


def test_hmiscehentai(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.HMisc_EHentai)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == 'Persona 4: Golden Characters'
    assert result.urls == []
    assert result.author == 'Unknown'

def test_twitter(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Twitter)
    result = SauceNao().from_url('https://example.com/')[0]

    assert result.title == '2017-06-26T11:09:04Z'
    assert result.urls == ['https://twitter.com/i/web/status/879295443850506242']
    assert result.author == 'petty_lily_xxx'
    assert type(result) is BasicSauce

def test_artstation(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.Artstation)
    result = SauceNao().from_url('http://example.com/')[0]

    assert result.title == 'Adnachiel Arknights Fanart'
    assert result.urls == ['https://www.artstation.com/artwork/OoyP0e']
    assert result.author == 'Rclouds 96'
    assert type(result) is BasicSauce

def test_furaffinity(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.FurAffinity)
    result = SauceNao().from_url('http://example.com')[0]

    assert result.title == 'playtime'
    assert result.urls == ['https://www.furaffinity.net/view/14385432']
    assert result.author == 'writersmask'
    assert type(result) is BasicSauce

def test_furry_network(mocked_responses):
    mocked_responses.add(responses.POST, SAUCENAO_URL, json=e.FurAffinity)
    result = SauceNao().from_url('http://example.com')[0]

    assert result.title == 'playtime'
    assert result.urls == ['https://www.furaffinity.net/view/14385432']
    assert result.author == 'writersmask'
    assert type(result) is BasicSauce 

