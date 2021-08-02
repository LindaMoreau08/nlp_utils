import nlp_utils.simple_tokenizer as tokenizer

debug = True


def test_tokenizer():
    text = "this is a test"
    tokens = tokenizer.tokenize(text)
    if debug:
        print(tokens)
    assert tokens == ["this", " ", "is", " ", "a", " ", "test"]


# it 'can join token patterns with and without emoticon patterns'
def test_join_token_patterns():
    with_emo_result = tokenizer.join_patterns(ignore_emoticons=False)
    no_emo_result = tokenizer.join_patterns(ignore_emoticons=True)
    assert with_emo_result != no_emo_result


def test_rgx_tokenize():
    text = "Now, this is a test!"
    tokens = tokenizer.tokenize(text)
    if debug:
        print(tokens)
    assert tokens == ['Now', ',', ' ', 'this', ' ', 'is', ' ', 'a', ' ', 'test', '!']


def test_stopwords():
    assert tokenizer.is_stopword('the')
    assert not tokenizer.is_stopword('thesis')


def test_extract_emails():
    results = tokenizer.extract_emails("to: jon@doe.com from: jane-nodoe@alive.org")
    assert results == ['jon@doe.com',  'jane-nodoe@alive.org']
    results = tokenizer.extract_emails("nothing to be found")
    assert results == []


def test_contains_emails():
    assert tokenizer.contains_email("to: jon@doe.com from: jane-nodoe@alive.org")
    assert not tokenizer.contains_email("nothing here")


def test_is_email():
    assert not tokenizer.is_email("to: jon@doe.com from: jane-nodoe@alive.org")
    assert tokenizer.is_email("jon@doe.com")


def test_extract_urls():
    results = tokenizer.extract_urls("go to www.doe.com or https://blah.de")
    assert results == ['www.doe.com',  'https://blah.de']
    results = tokenizer.extract_urls("nothing to be found")
    assert results == []


def test_contains_urls():
    assert tokenizer.contains_url("go to www.doe.com or https://blah.de")
    assert not tokenizer.contains_url("nothing here")


def test_is_url():
    assert not tokenizer.is_url("go to www.doe.com or https://blah.de")
    assert tokenizer.is_url("www.doe.com")


def test_extract_hashtags():
    results = tokenizer.extract_hashtags("I #disprefer #winter, so there")
    assert results == ['#disprefer',  '#winter']
    results = tokenizer.extract_hashtags("nothing to be found")
    assert results == []


def test_contains_hashtags():
    assert tokenizer.contains_hashtag("I #disprefer #winter, so there")
    assert not tokenizer.contains_hashtag("nothing here")


def test_is_hashtag():
    assert not tokenizer.is_hashtag("go to www.doe.com or https://blah.de")
    assert tokenizer.is_hashtag("#winter")
    assert not tokenizer.is_hashtag("#winter,")


def test_extract_usernames():
    results = tokenizer.extract_usernames("@priscilla are you priscilla@hotmail?")
    assert results == ['@priscilla']
    results = tokenizer.extract_usernames("nothing to be found")
    assert results == []


def test_contains_usernames():
    assert tokenizer.contains_username("@priscilla are you priscilla@hotmail?")
    assert not tokenizer.contains_username("nothing here priscilla@hotmail?")


def test_is_username():
    assert not tokenizer.is_username("priscilla@hotmail")
    assert tokenizer.is_username("@priscilla")


def test_extract_emojis():
    results = tokenizer.extract_emojis("😴 we   👩‍👧‍👧  have flags 🇬🇧")
    assert results == ['😴', '👩‍👧‍👧', '🇬🇧']
    results = tokenizer.extract_emojis("nothing to be found")
    assert results == []


def test_contains_emojis():
    assert tokenizer.contains_emoji("go to www.doe.com or   👩‍👧‍👧 https://blah.de")
    assert not tokenizer.contains_emoji("nothing here")


#TODO: fix the emoji ranges so symbols that are not emoticons can be recognized
def test_is_emoji():
    assert not tokenizer.is_emoji("go 😴to www.doe.com or https://blah.de")
    assert tokenizer.is_emoji("😴")
    #assert not tokenizer.is_emoji("®")


def test_extract_emoticons():
    results = tokenizer.extract_emoticons(":-D we   :-b have no flags D-:")
    assert results == [':-D', ':-b', 'D-:']
    results = tokenizer.extract_emoticons("nothing to be found")
    assert results == []


def test_contains_emoticons():
    assert tokenizer.contains_emoticon(":-D we   :-b have no flags D-:")
    assert not tokenizer.contains_emoticon("nothing here")


def test_is_emoticon():
    assert not tokenizer.is_emoticon(":-D we   :-b have no flags D-:")
    assert tokenizer.is_emoticon(":-D")
    assert tokenizer.is_emoticon("D-:")


def test_is_emoji_or_emoticon():
    assert not tokenizer.is_emoji_or_emoticon(":-D we   :-b have no flags D-:")
    assert not tokenizer.is_emoji_or_emoticon("Bob")
    assert tokenizer.is_emoji_or_emoticon(":-D")
    assert tokenizer.is_emoji_or_emoticon("D-:")
    assert tokenizer.is_emoji_or_emoticon("😴")
    assert tokenizer.is_emoji_or_emoticon("🚩")


def test_all_emoji_chars():
    assert tokenizer.all_emoji_chars(" 😴")


def test_all_symbol_or_punct():
    assert tokenizer.all_symbol_or_punct('%$#@)')


def test_has_contraction():
    assert tokenizer.has_contraction("can't")


def test_is_acronym():
    assert tokenizer.is_acronym('U.S.A.')


def test_is_contraction():
    assert tokenizer.is_contraction("isn't")


def test_is_digits():
    assert tokenizer.is_digits('12345')


def test_is_flag():
    assert tokenizer.is_flag('⚑')


def test_is_money():
    assert tokenizer.is_money('$42.00')


def test_is_normtag():
    assert tokenizer.is_normtag('norm_quotation')


def test_is_ordinal():
    assert tokenizer.is_ordinal('51st')


def test_is_punct():
    assert tokenizer.is_punct('?!')


def test_is_quotation():
    assert tokenizer.is_quotation("\"crazy\"")


def test_is_slash_abbreviation():
    assert tokenizer.is_slash_abbreviation('b/c')


def test_is_space():
    assert tokenizer.is_space('    ')


def test_is_symbol():
    assert tokenizer.is_symbol('©')


def test_is_word():
    assert tokenizer.is_word('cheese-puff')


def test_symbol_mark_punct_count():
    assert tokenizer.symbol_mark_punct_count("$43.1!") == 3


def test_get_token_type():
    assert tokenizer.get_token_type(' ') == [tokenizer.TT_space, '']
    assert tokenizer.get_token_type('«blah»') == [tokenizer.TT_quotation, '']
    assert tokenizer.get_token_type('norm_whatever') == [tokenizer.TT_normtag, '']
    assert tokenizer.get_token_type('hungry@evening.now') == [tokenizer.TT_email, '']
    assert tokenizer.get_token_type('https://www.blah.net') == [tokenizer.TT_url, '']
    assert tokenizer.get_token_type('a.b.c.') == [tokenizer.TT_word, 'acronym']
    assert tokenizer.get_token_type('b/d') == [tokenizer.TT_word, 'abbreviation']
    assert tokenizer.get_token_type('frog') == [tokenizer.TT_word, '']
    assert tokenizer.get_token_type('#clean_water') == [tokenizer.TT_hashtag, '']
    assert tokenizer.get_token_type('42nd') == [tokenizer.TT_number, tokenizer.TS_ordinal]
    assert tokenizer.get_token_type('42') == [tokenizer.TT_number, tokenizer.TS_cardinal]
    assert tokenizer.get_token_type('$42.00') == [tokenizer.TT_number, tokenizer.TS_money]
    assert tokenizer.get_token_type('@mybad') == [tokenizer.TT_username, '']
    assert tokenizer.get_token_type("🇬🇧") == [tokenizer.TT_emoji, tokenizer.TS_flag]
    assert tokenizer.get_token_type('😴') == [tokenizer.TT_emoji, tokenizer.TS_emoji]
    assert tokenizer.get_token_type(':-)') == [tokenizer.TT_emoji, tokenizer.TS_emoticon]
    assert tokenizer.get_token_type('?!') == [tokenizer.TT_punct, '']
    assert tokenizer.get_token_type('®') == [tokenizer.TT_symbol, '']

# TODO: Add legacy tests
# TODO: