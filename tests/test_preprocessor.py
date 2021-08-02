import pytest
from nlp_utils.preprocessor import Preprocessor

verbose = True


@pytest.fixture(scope='module')
def my_preppy():
    return Preprocessor()


@pytest.fixture(scope='module')
def test_hashtags():
    # TODO: load hashtag file here
    return ['#hashtag1', ' #hashtag2']


def test_preprocessor_tokenize(my_preppy):
    doc_span = my_preppy.tokenize("This #yearOfHell needs to end @Trump #GetOut!")
    if verbose:
        for token in doc_span:
            print(token)
    assert len(doc_span) == 8


def test_preprocessor_trim_tweet(my_preppy):
    normy = my_preppy.normalize_tweet("  -- |#dems are weak #polarizing #politics https://blah.com")
    assert normy == '#dems are weak'


# TODO: discuss whether to try to kep the last hashtag based on non-hash before it
def test_preprocessor_trim_tweet_stop_correctly(my_preppy):
    normy = my_preppy.normalize_tweet("  -- |#dems are weak #polarizing liberal #politics https://blah.com")
    assert normy == '#dems are weak #polarizing liberal'


# TODO: decide whether keeping spaces and newlines is worth any effort
def test_preprocessor_trim_tweet_real(my_preppy):
    input = "Well folks, we are open til 4, last orders at 330. Come on down for coffee, cake, brunch or lunch.\nWe have steak pies & veggie pies but they are going fast so don’t miss out!  #glasgow #glasgowcafe #glasgowcakes #glasgowsouthside #treatyourself #hogmanay #cafe #food #cake"
    normy = my_preppy.normalize_tweet(input)
    if verbose:
        print(normy)
    assert normy == "Well folks, we are open til 4, last orders at 330. Come on down for coffee, cake, brunch or lunch. We have steak pies & veggie pies but they are going fast so don’t miss out!"


def test_hashtag2word(my_preppy):
    assert my_preppy.hashtag2word('  #Butter ') == 'butter'


def test_hashtag2word_harder(my_preppy):
    assert my_preppy.hashtag2word('#life_s0_good') == 'life so good'


def test_hashtag2word_even_harder(my_preppy):
    assert my_preppy.hashtag2word('#life_s0_good_live4love') == 'life so good live for love'


def test_check_word_non_word(my_preppy):
    result = my_preppy.check_word('live2love')
    if verbose:
        print(result)
    assert result is None


def test_check_word_real_word(my_preppy):
    result = my_preppy.check_word('live')
    if verbose:
        print(result)
    assert result == 'live'


def test_check_word_word_with_nums(my_preppy):
    result = my_preppy.check_word('lové')
    if verbose:
        print(result)
    assert result == 'love'


def test_check_word_word_with_nums_and_letters(my_preppy):
    result = my_preppy.check_word('looOOove')
    if verbose:
        print(result)
    assert result == 'love'


word_variants = ['love', 'l0ve', 'looOOove', 'loooove', 'lové', 'l0000ve', 'looooooooooooove']


@pytest.mark.parametrize("word_var", word_variants)
def test_check_word(my_preppy, word_var):
    result = my_preppy.check_word(word_var)
    if verbose:
        print(result)
    assert result in ['love', 'loove']


def test_normalize_tweet_wordify_hashtags(my_preppy):
    tweet = " -- | Hey @friend I #love2live fast and free #blah #blah"
    result = my_preppy.normalize_tweet(tweet, hashtag2words=True)
    assert result == 'Hey @friend I love to live fast and free'


def test_normalize_tweet_wordify_hashtags_space_yuk(my_preppy):
    tweet = "@Bob\n -- | Hey @friend\n I\t love 2 live fast\n and free #blah #blah\n\n\t"
    result = my_preppy.normalize_tweet(tweet)
    assert result == '@Bob - Hey @friend I love 2 live fast and free'


def test_normalize_spaces_in_tweet(my_preppy):
    tweet = "@AmyMek \n SAD BUT TRUE☹️ #Election2020 #ElectionNight #Elections2020 https://t.co/LNakiqRa8M"
    result = my_preppy.normalize_tweet(tweet)
    assert result == "@AmyMek SAD BUT TRUE☹️"


def test_text_prep(my_preppy):
    output = my_preppy.normalize_tweet("RT @Mike --| this is\n a blah\t\ttweet!!!")
    assert output == "this is a blah tweet!!!"