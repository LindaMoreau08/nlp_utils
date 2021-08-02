import regex
import unicodedata
from collections import OrderedDict
import nlp_utils.simple_tokenizer as token_tests


def split_by_category(smashed_word, lowercase=False):
    smashed_word = smashed_word.strip('#@ _')
    smashed_word = regex.sub(r'_+', '_', smashed_word)
    split_hashtag = []
    cur_string = smashed_word[0:1]
    cur_start = 1
    prev_cat = unicodedata.category(smashed_word[0])
    for i in range(1, len(smashed_word)):
        cur_cat = unicodedata.category(smashed_word[i])
        if (i == cur_start and prev_cat in ['Ll', 'Lu', 'L']) or cur_cat == prev_cat:
            cur_string += smashed_word[i]
            prev_cat = cur_cat
        else:
            if lowercase:
                cur_string = cur_string.lower()
            if not token_tests.is_punct(cur_string):
                split_hashtag.append(cur_string)
            cur_string = smashed_word[i]
            prev_cat = cur_cat
            if prev_cat not in ['Lu', 'Ll', 'L']:
                cur_start = i + 2
            else:
                cur_start = i + 1
    if cur_string:
        if lowercase:
            cur_string = cur_string.lower()
        split_hashtag.append(cur_string)
    return split_hashtag


def pass_numbers(word):
    if regex.fullmatch(r"^\p{N}$",word):
        return word
    return None


def orig_word(word):
    return word


def norm_word(word):
    return unicodedata.normalize('NFKD', word.strip())


def norm_for_retrieval(word,
                       remove_hyphens:bool = True,
                       remove_underscores: bool = True,
                       remove_diacritics: bool = True):
    word = unicodedata.normalize('NFKD', word.strip().lower())
    if remove_hyphens:
        word = word.replace('-', '')
    if remove_underscores:
        word = word.replace('_', '')
    word = regex.sub(r"[\s\t\n\p{Z}]+", ' ', word)


def norm_for_word_recovery(token, allow_two_repeats=True):
    token = unicodedata.normalize('NFKD', token.strip().lower())
    token = denumify_word(token)
    token = remove_repeats(token, allow_two_repeats)
    return token


def dediacritize(word):
    word = unicodedata.normalize('NFKD', word.strip())
    return regex.sub(r"[\p{Mn}]", "", word)


# TODO:  modify this to produce permutations
def denumify_word(word):
    word = word.replace('0', 'o')
    word = word.replace('1', 'i')
    word = word.replace('8', 'a')
    word = word.replace('4', ' for ')
    word = word.replace('2', ' to ')
    word = regex.sub(r"\s+", " ", word)
    return word.strip()


def remove_repeats(word, allow_two=True, lowercase=True):
    if lowercase:
        word = word.strip().lower()
    if allow_two:
        word = regex.sub(r"([\p{L}\p{N}])\1\1+", "\\1\\1", word)
    else:
        word = regex.sub(r"([\p{L}\p{N}])\1+", "\\1", word)
    return word


def sort_dict(data_dict, by_value=True, reverse_order=True):
    if by_value:
        ordered_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[1], reverse=reverse_order))
    else:
        ordered_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[0], reverse=reverse_order))
    return ordered_dict


