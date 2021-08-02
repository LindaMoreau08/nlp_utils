# -*- coding: utf-8 -*-

# TODO: turn this into a class and implement it correctly!

import numpy
import regex
import stopwords
from w3lib.html import replace_entities


lang_stopwords = stopwords.get_stopwords('en')

NORM_prefix = 'norm_'

# TOKEN TYPES (TT_)l
TT_email = 'email'
TT_emoji = 'emoji'
TT_hashtag = 'hashtag'
TT_normtag = 'norm_tag'
TT_number = 'number'
TT_punct = 'punct'
TT_quotation = 'quotation'
TT_space = 'space'
TT_symbol = 'symbol'
TT_url = 'url'
TT_username = 'username'
TT_unk = 'unk'
TT_word = 'word'

# TOKEN SUBTYPES
TS_emoticon = 'emoticon'
TS_emoji = 'emoji'
TS_flag = 'flag'
TS_ordinal = 'ordinal'
TS_cardinal = 'cardinal'
TS_money = 'monetary'
TS_acronym = 'acronym'
TS_abbreviation = 'abbreviation'

# single codepoint flags
Base_flags = ['⚐', '⚑', '⛳', '⛿', '🎌', '🏁', '🏱', '🏳', '🏴', '🚩']

Space_reguex = r'[\p{Z}\p{C}]+'

# TODO: add from unicode chart
Punct_pairs = {")": "(", "]": "[", "}": "{", "»": "«", ">": "<", "´": "`", "/": "\\"}
Char_subs = {"0": 'o', "1": 'i', "3": 'e', "4": 'a', "5": "s", "7": 't', "8": 'a', "9": 'g', "@": 'a', "$": 's', "!": 'i'}
emoji = r'[\p{Emoji=Yes}&&[^\u00A9\u00Ae\u0030-\u0039\u203c\u2049\u2122]]'

emoticon_1 = r'(?:[:;][*\-]?[Ddpb\)\(\}\{o\]])|(?:[Ddpb\)\(\}\{o\]][*\-]?[:;])'
emoticon_2 = r'[03578BbPpOODdXx×VvÞþ][\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{Lm}\p{InBOX_DRAWING}]+[03578BbPpOODdXx×VvÞþ]?0?3?'
emoticon_3 = r'[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{InBOX_DRAWING}]+[\p{L}\p{N}]{1,2}[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{Lm}\p{InBOX_DRAWING}]*[oO0.]?3?[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{InBOX_DRAWING}]*'

patterns = {
    'html_codes': r'((?:&(?:#?[0-9a-f]+|[a-z]+);)',
    'twitter_usernames': r'(?:(?<![\p{L}\p{N}])@+[\w_]+)',
    'hashtags': r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',
    'norm_tags': r'(?:norm__?[_A-Z]+)',
    'tags': r'(?:<\w+\/>)',
    'email': r'(?:\b[\p{L}\p{N}][\p{L}\p{N}._%+\!-]+@(?:[A-Za-z0-9.\-]+\.[A-Za-z]{2,4}|\[?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]?))',
    'url': r'(?:(?:http|ftp|file|mailto|data|irc)s?:\/\/\S+)|(?:www2?\.\S+)|(?:\S+\.(?:com|edu|gov|org|info|biz|mil|net|name|museum|[a-z]{2}\b)(?:\/\S+)?)',
    'acronyms': r'(?:\b\p{L}{1,3}\.(?:\p{L}{1,3}\.)+(?:\p{L}\b)?)|(?:\b[\p{L}&&[^aeiouAEIOU]]{1,3}\.)|(?:\b[aeiouAEIOU][\p{L}&&[^aeiouAEIOU]]{1,3}\.)|(?:\b\p{L}\.)',
    'slash_abbreviation': r'(?:\p{L}\/\p{L}(?:\/\p{L})*)',
    'emoticon_1': r'(?:(?<![\p{L}\p{N}])[03578BbPpOODdXx×VvÞþ][\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{Lm}\p{InBOX_DRAWING}]+[03578BbPpOODdXx×VvÞþ]?0?3?(?![\p{L}\p{N}\p{P}\p{S}]))',
    'emoticon_2': r'(?:(?<![\p{L}\p{N}])[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{InBOX_DRAWING}]+[\p{L}\p{N}]{1,2}[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{Lm}\p{InBOX_DRAWING}]*[oO0.]?3?[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}\p{InBOX_DRAWING}]*(?![\p{L}\p{N}\p{P}]))',
    'ordinals': r'(?:\b[0-9]*(?:1st|2nd|3rd|11th|12th|13th|[4-9]th)\b)',
    'masked_words_numalpha': r'(?:\b\p{N}{1,2}\p{L}[\p{L}\p{N}\p{M}@$#*+✞]*)',
    'digits': r'(?:[.+\-]?\p{N}+(?:[.,\-:\/]*\p{N}+)*)',
    'contractions': r'(?:(?:n[\'’]t\b)|(?:[\'’](?:[sdm]|(?:ld)|(?:ll)|(?:re)|(?:ve)|(?:nt))\b))',
    'taboo_punct': r'(?:[$*@][\p{L}\p{M}\p{N}@$#*+✞]+(?:[\-\'’,.][\p{L}\p{M}\p{N}]+)*)',
    'words': r'(?:\p{L}[\p{L}\p{M}\p{N}@$#*+✞]*(?:[\-\'’][\p{L}\p{M}\p{N}@$#*+✞]+)*)',
    'punct_repeat': r'(?:(?:\.\.+|--+|__+|~~+|[!?][!?]+|\*\*+|//+|##+)[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}°\p{InBOX_DRAWING}\p{InGEOMETRIC_SHAPES}]*)',
    'punct': r'(?:[\p{P}\p{M}\p{Sm}\p{Sc}\p{Sk}°\p{InBOX_DRAWING}\p{InGEOMETRIC_SHAPES}]+)',
    'key_caps': r'(?:[#\*0-9]\ufe0f?\u20e3)',
    'flags': r'(?:[\U0001F1E6-\U0001F1FF]{2})|(?:[⚐⚑⛳⛿🎌🏁🏱🏳🏴🚩🏴](?:[\u200d\uFE0F]{1,2}\p{So}\uFE0F?)?)',
    'emojis': r'(?:'+emoji+r'[\U0001f3fb-\U0001f3ff]?\uFE0F?(?:\u200D'+emoji+r'[\U0001f3fb-\U0001f3ff]?\uFE0F?)*)',
    'symbols': r'(?:\p{S}+)',
    'space': r'(?:[\p{Z}\p{C}]))'
}


def join_patterns(ignore_emoticons=False, ignore_taboo=False, split_punct=True, split_repeated_punct=False):
    token_reguex = ''
    patterns_added = 0
    for pattern_name, pattern in patterns.items():
        pattern_name = pattern_name
        if split_repeated_punct and pattern_name == 'punct_repeat':
            continue
        if split_punct and pattern_name == 'punct':
            pattern = r'(?:\p{P})'
        if ignore_emoticons and pattern_name.find('emoticon') >= 0:
            continue
        if ignore_taboo and pattern_name.find('taboo') >= 0:
            continue
        if patterns_added > 0:
            token_reguex += '|'
        token_reguex += pattern
        patterns_added += 1
    return regex.compile(token_reguex, regex.V1)


big_regex = join_patterns()


def tokenize(text):
    return regex.findall(big_regex, text)


# Assemble token patterns into various regexes for use by the token tests.
NORM_TAG_REGEX = regex.compile(patterns['norm_tags'], regex.V1)
IS_NORM_TAG_REGEX = regex.compile('^norm_(?<norm_opt>[a-zA-Z_]+)$', regex.V1)
TOKEN_REGEX = big_regex
EMAIL_REGEX = regex.compile(patterns['email'], regex.V1)  # contains email
IS_EMAIL_REGEX = regex.compile('^' + patterns['email'] + '$', regex.V1)
URL_REGEX = regex.compile(patterns['url'], regex.IGNORECASE|regex.V1)  # contains url
IS_URL_REGEX = regex.compile('^' + patterns['url'] + '$', regex.IGNORECASE|regex.V1)
IS_DIGITS_REGEX = regex.compile("^" + patterns['digits'] + "$", regex.V1)
IS_MONEY_REGEX = regex.compile(r'^\p{Sc}' + patterns['digits'] + "$", regex.V1)
DIGITS_REGEX = IS_DIGITS_REGEX  # TODO: for Salton, update when Salton changes have been pushed
IS_ORDINAL_REGEX = regex.compile("^" + patterns['ordinals'] + "$", regex.V1)
IS_SPACE_REGEX = regex.compile('^' + Space_reguex + '$', regex.V1)
SPACE_REGEX_SPLIT = regex.compile(Space_reguex, regex.V1)
SPACE_REGEX_KEEP = regex.compile('(' + Space_reguex + ')', regex.V1)
IS_PUNCT_REGEX = regex.compile(r'^\p{P}+$', regex.V1)  # sequence of punctuation marks
IS_SYMBOL_REGEX = regex.compile("^" + patterns['symbols'] + "$", regex.V1)
IS_WORD_REGEX = regex.compile("^" + patterns['words'] + "$", regex.V1)
IS_ACRONYM_REGEX = regex.compile("^" + patterns['acronyms'] + "$", regex.V1)
STRIP_REGEX = r'^(?:[\s"\']|\\")+|(?:[\s"\']|\\")+$'  # leading or trailing quotes (possibly escaped) and spaces
QUOTATION_REGEX = r'["“”][^"“”]+?["“”]'
IS_QUOTATION_REGEX = regex.compile(r'^["“”«][^"“”«»]+?["“”»]$', regex.V1)
USERNAME_REGEX = regex.compile(patterns['twitter_usernames'], regex.V1)
IS_USERNAME_REGEX = regex.compile('^' + patterns['twitter_usernames'] + '$', regex.V1)
HASHTAG_REGEX = regex.compile(patterns['hashtags'], regex.V1)
IS_HASHTAG_REGEX = regex.compile('^' + patterns['hashtags'] + '$', regex.V1)
EMOTICON_REGEX = regex.compile(patterns['emoticon_1'] + '|' + patterns['emoticon_2'], regex.V1)
IS_EMOTICON_REGEX = regex.compile('^((?:' + emoticon_1 + ')|(?:' + emoticon_2 + ')|(?:' + emoticon_3 + '))$', regex.V1)
EMOJI_REGEX = regex.compile(patterns['key_caps'] + '|' + patterns['flags'] + '|' + patterns['emojis'], regex.V1)
IS_EMOJI_REGEX = regex.compile(
    '^' + patterns['key_caps'] + '|' + patterns['flags'] + '|' + patterns['emojis'] + '$', regex.V1)
CONTRACTION_REGEX = regex.compile(r'(?:(?:n[\'’]t\b)|(?:[\'’](?:[sdm]|(?:ld)|(?:ll)|(?:re)|(?:ve)|(?:nt))\b))', regex.V1)
IS_CONTRACTION_REGEX = regex.compile(r'^(?:(?:n[\'’]t\b)|(?:[\'’](?:[sdm]|(?:ld)|(?:ll)|(?:re)|(?:ve)|(?:nt))\b))$', regex.V1)
CONTRACTION_SPLIT_REGEX = regex.compile(
    r'(?:^(?<word>\p{L}[\p{L}\p{M}]*?)(?<contraction>(?:n[\'’]t)|(?:[\'’](?:s|d|m|ld|ll|re|ve|nt)))$)', regex.V1)
FLAG_REGEX = regex.compile(patterns['flags'], regex.V1)
IS_FLAG_REGEX = regex.compile('^' + patterns['flags'] + '$', regex.V1)
KEY_CAP_REGEX = regex.compile(patterns['flags'], regex.V1)
IS_KEY_CAP_REGEX = regex.compile('^' + patterns['flags'] + '$', regex.V1)
IS_SLASH_ABBREVIATION_REGEX = regex.compile('^' + patterns['slash_abbreviation'] + '$', regex.V1)


# TODO: this is not terribly efficient to scan with so many regexes
def pre_process_text(text, options):
    if options['norm_codes']:
        text = replace_entities(text)
    if options['norm_quotations']:
        text = regex.sub(QUOTATION_REGEX, "#{NORM_QUOTATION}", text)
    if options['norm_space'] and options['keep_space']:
        text = regex.sub(SPACE_REGEX_SPLIT, ' ', text)
    return text


def regex_tokenize(text, keep_space=False, norm_space=False):
    rgx_tokenize(text, keep_space=keep_space, norm_space=norm_space)


def rgx_tokenize(text, keep_space=False, norm_space=False, pre_process=True, ignore_emoticons=False, split_punct=False,
                 split_repeated_punct=False):
    if pre_process:
        text = pre_process_text(text, {keep_space: keep_space, norm_space: norm_space})
    tokenization_reguex = join_patterns(ignore_emoticons=ignore_emoticons, split_punct=split_punct,
                                        split_repeated_punct=split_repeated_punct )
    if keep_space:
        tokens = text.scan(tokenization_reguex)
    else:
        tokens = text.split(SPACE_REGEX_SPLIT)
    tokens = map(lambda x: regex.findall(tokenization_reguex, x), tokens)
    tokens = numpy.array(tokens).flatten()
    # tokens = retokenize(tokens, options)
    return tokens


def retokenize(tokens, opts):
    tokenization_reguex = join_patterns(ignore_emoticons=True, ignore_taboo=True, split_punct=opts['split_punct'],
                                        split_repeated_punct=opts['split_repeated_punct']) #if ignore_emoticons
    retokenized = []
    for token in tokens:
        token_type = get_token_type(token)
        if is_money(token):
            retokenized.append(token.scan(tokenization_reguex))
        elif is_taboo(token) or token_type[0] != TT_unk:
            retokenized.append(token)
        else:
            retokenized.append(token.scan(tokenization_reguex))
    new_tokens = numpy.array(retokenized).flatten()
    return new_tokens


# TODO: Port taboo list
def is_taboo(text):
    if text in ['shit', 'hell']:
        return True
    return False


def is_stopword(text):
    return text.strip().lower() in lang_stopwords


# TODO: implement this loading elsewhere
def is_lang_stopword(text, lang='en'):
    if lang != 'en':
        the_stopwords = stopwords.get_stopwords(lang)
    return is_stopword(text)

# TODO: implement features
#def has_feature(text, feature, language):
#    my_featurizer.has_feature?(text, feature, language)


def extract_emails(text):
    return regex.findall(EMAIL_REGEX, text)


def contains_email(text):
    return regex.search(EMAIL_REGEX, text)


def is_email(text):
    return regex.match(IS_EMAIL_REGEX, text.strip()) is not None


def extract_urls(text):
    return regex.findall(URL_REGEX, text)


def contains_url(text):
    return regex.search(URL_REGEX, text)


def is_url(text):
    return regex.match(IS_URL_REGEX, text.strip())


def extract_hashtags(text):
    return regex.findall(HASHTAG_REGEX, text)


def contains_hashtag(text):
    return regex.search(HASHTAG_REGEX, text)


def is_hashtag(text):
    return regex.match(IS_HASHTAG_REGEX, text.strip())


def extract_usernames(text):
    return regex.findall(USERNAME_REGEX, text)


def contains_username(text):
    return regex.search(USERNAME_REGEX, text)


def is_username(text):
    return regex.match(IS_USERNAME_REGEX, text.strip())


def extract_emojis(text):
    return regex.findall(EMOJI_REGEX, text)


def contains_emoji(text):
    return regex.search(EMOJI_REGEX, text)


def is_emoji(text):
    return regex.match(IS_EMOJI_REGEX, text.strip())


def extract_emoticons(text):
    return regex.findall(EMOTICON_REGEX, text)


def contains_emoticon(text):
    return regex.search(EMOTICON_REGEX, text)


# TODO: reimplement emoticon file reading with detection of unknown emoticons, etc.
def is_emoticon(text):
    return regex.match(IS_EMOTICON_REGEX, text.strip())


def is_emoji_or_emoticon(text):
        return is_emoji(text) or is_emoticon(text)


def is_digits(text):
    return regex.match(IS_DIGITS_REGEX, text.strip())


def is_money(text):
    return regex.match(IS_MONEY_REGEX, text.strip())


def is_ordinal(text):
    return regex.match(IS_ORDINAL_REGEX, text.strip())


def is_space(text):
    return regex.match(IS_SPACE_REGEX, text)


def is_punct(text):
    return regex.match(IS_PUNCT_REGEX, text)


def is_symbol(text):
    return regex.match(IS_SYMBOL_REGEX, text)


def is_normtag(text):
    return regex.match(IS_NORM_TAG_REGEX, text)


def is_word(text):
    return regex.match(IS_WORD_REGEX, text)


def is_acronym(text):
    return regex.match(IS_ACRONYM_REGEX, text)


def is_slash_abbreviation(text):
    return regex.match(IS_SLASH_ABBREVIATION_REGEX, text)


def is_quotation(text):
    text = text.strip().lower()
    return text == "#{NORM_prefix}#{TT_quotation}".lower() or regex.match(IS_QUOTATION_REGEX, text)


def has_contraction(text):
    return regex.search(CONTRACTION_REGEX, text)


def is_contraction(text):
    return has_contraction(text)


def is_flag(text):
    return text.strip() in Base_flags or regex.match(IS_FLAG_REGEX, text.strip())


def all_symbol_or_punct(text, ignore_space=True):
    if ignore_space:
        text = regex.sub(r'\p{Z}', '', text)
    return regex.match(r'^[\p{P}\p{S}\p{M}\p{Lm}]+$', text)


def all_emoji_chars(text, ignore_space=True):
    if ignore_space:
        text = regex.sub(r'\p{Z}', '', text)
    return regex.match(r'^[へ\p{P}\p{S}\p{M}\p{Lm}\p{In_BOX_DRAWING}\p{In_GEOMETRIC_SHAPES}]+$', text)


# TODO:  consider whether \p{Lm} belongs
def symbol_mark_punct_count(text):
    match_count = 0
    matches = regex.findall(r'[\p{P}\p{M}\p{S}]', text)
    if matches:
        match_count = len(matches)
    return match_count


# get the token type and subtype, if applicable
def get_token_type(token_text):
    if is_space(token_text):
        return [TT_space, '']
    if is_quotation(token_text):
        return [TT_quotation, '']
    if is_normtag(token_text):
        return [TT_normtag, '']
    if is_email(token_text):
        return [TT_email, '']
    if is_url(token_text):
        return [TT_url, '']
    if is_acronym(token_text):
        return [TT_word, TS_acronym]
    if is_slash_abbreviation(token_text):
        return [TT_word, TS_abbreviation]
    if is_word(token_text):
        return [TT_word, '']
    if is_hashtag(token_text):
        return [TT_hashtag, '']
    if is_ordinal(token_text):
        return [TT_number, TS_ordinal]
    if is_digits(token_text):
        return [TT_number, TS_cardinal]
    if is_money(token_text):
        return [TT_number, TS_money]
    if is_username(token_text):
        return [TT_username, '']
    if is_flag(token_text):
        return [TT_emoji, TS_flag]
    if is_emoji(token_text):
        return [TT_emoji, TS_emoji]
    if is_emoticon(token_text):
        return [TT_emoji, TS_emoticon]
    if is_punct(token_text):
        return [TT_punct, '']
    if is_symbol(token_text):
        return [TT_symbol, '']
    return [TT_unk, '']
