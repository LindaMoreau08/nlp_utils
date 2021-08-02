import pytest
from collections import OrderedDict
import nlp_utils.string_utils as su

hashtag_standard = ['#LiveToLove', '#liveToLove', '#live_to_love', '#live_to__love', '#live_to_love__']
hashtag_num_words = ['live2love', 'LIVE2love', 'live_2_love', 'live___2___love'];
hashtag_num_nums = ['#election_2020', '#election2020', '#2020election'];
hashtag_num_chars = ['#l0ve','l0000ve', '#h8ters'];


def test_remove_repeats_two():
    assert su.remove_repeats("sooooooooo") == "soo"


def test_remove_repeats_one():
    assert su.remove_repeats("soooOOoooo", allow_two=False) == "so"


def test_dediacritize():
    assert su.dediacritize("café") == "cafe"


def test_split_by_rule_1():
    result = su.split_by_category("1live4love2", lowercase=True)
    assert result == ['1', 'live','4','love','2']


def test_split_by_rule_2():
    result = su.split_by_category("1_live_4_love_2", lowercase=True)
    assert result == ['1', 'live','4','love','2']


@pytest.mark.parametrize("hashtag_forms", hashtag_standard)
def test_split_by_category_permutations(hashtag_forms):
    result = su.split_by_category(hashtag_forms, lowercase=True)
    assert result == ['live','to','love']


@pytest.mark.parametrize("hashtag_number_words", hashtag_num_words)
def test_split_by_category_number_words(hashtag_number_words):
    result = su.split_by_category(hashtag_number_words, lowercase=True)
    assert result == ['live','2','love']


@pytest.mark.parametrize("hashtag_numbers", hashtag_num_nums)
def test_split_by_category_number_words(hashtag_numbers):
    result = su.split_by_category(hashtag_numbers, lowercase=True)
    assert result in [['election', '2020'], ['2020', 'election']]


def test_denumify_word():
    result = su.denumify_word('s0')
    assert result == 'so'


def test_sort_dict_defaults_descending_by_value():
    test_freqs = {'dog': 4, 'zebra': 3, 'aardvark': 2, 'camel': 1}
    result = su.sort_dict(test_freqs)
    assert result == OrderedDict({'dog':4, 'zebra':3, 'aardvark':2, 'camel':1 })


def test_sort_dict_ascending_by_value():
    test_freqs = {'dog': 4, 'zebra': 3, 'aardvark': 2, 'camel': 1}
    result = su.sort_dict(test_freqs, reverse_order=False)
    assert result == OrderedDict({'camel': 1, 'aardvark': 2, 'zebra': 3, 'dog': 4})


def test_sort_dict_descending_by_value():
    test_freqs = {'dog': 4, 'zebra': 3, 'aardvark': 2, 'camel': 1}
    result = su.sort_dict(test_freqs, reverse_order=True)
    assert result == OrderedDict({'dog':4, 'zebra':3, 'aardvark':2, 'camel':1 })


def test_sort_dict_ascending_by_key():
    test_freqs = {'dog': 4, 'zebra': 3, 'aardvark': 2, 'camel': 1}
    result = su.sort_dict(test_freqs, by_value=False, reverse_order=False)
    assert result == OrderedDict({'aardvark': 2, 'camel': 1, 'dog': 4, 'zebra': 3 })


def test_sort_dict_descending_by_key():
    test_freqs = {'dog': 4, 'zebra': 3, 'aardvark': 2, 'camel': 1}
    result = su.sort_dict(test_freqs, by_value=False, reverse_order=True)
    assert result == OrderedDict({ 'zebra': 3, 'dog': 4, 'camel': 1, 'aardvark': 2 })
