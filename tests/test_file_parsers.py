import pytest

import nlp_utils.file_parsers as fp

pytest_temp = "pytest_temp"


def test_list_parser_one_element_per_line(tmpdir):
    list_data = "tomatoes\npeppers\nonions\ngarlic\n"
    my_fi = tmpdir.mkdir(pytest_temp).join("shopping_list.txt")
    my_fi.write(list_data)
    list_list = fp.load_list(my_fi.strpath)
    assert len(list_list) == 4


def test_list_parser_one_element_per_line_no_trailing_newline(tmpdir):
    list_data = "tomatoes\npeppers\nonions\ngarlic"
    my_fi = tmpdir.mkdir(pytest_temp).join("shopping_list.txt")
    my_fi.write(list_data)
    list_list = fp.load_list(my_fi.strpath)
    assert len(list_list) == 4


def test_list_parser_comma_delim_multiline(tmpdir):
    list_data = "tomatoes,peppers,onions,garlic\nchocolate, caramel, toffy\n"
    my_fi = tmpdir.mkdir(pytest_temp).join("shopping_list.txt")
    my_fi.write(list_data)
    list_list = fp.load_list(my_fi.strpath, delim=",", trim_elements=False)
    assert len(list_list) == 7
    assert 'caramel' not in list_list


def test_dict_parser_defaults(tmpdir):
    dict_data = "she|female\nher|female\nhers|female\nherself|female\nhe|male\nhim|male\nhis|male\nhimself|male"
    my_fi = tmpdir.mkdir(pytest_temp).join("gender_term_map.txt")
    my_fi.write(dict_data)
    dict_dict, errors = fp.load_dict(my_fi.strpath)
    assert len(dict_dict) == 8
    assert dict_dict['him'] == 'male'


def test_csv_dict_parser_defaults(tmpdir):
    dict_data = "she|female\nher|female\nhers|female\nherself|female\nhe|male\nhim|male\nhis|male\nhimself|male"
    my_fi = tmpdir.mkdir(pytest_temp).join("gender_term_map.txt")
    my_fi.write(dict_data)
    dict_dict, errors = fp.load_dict_from_csv(my_fi.strpath)
    assert len(dict_dict) == 8
    assert dict_dict['him'] == 'male'


def test_load_dict_from_jsonl(tmpdir):
    dict_data = '{"lemma": "postdoc", "label": "education_level"}\n{"lemma": "dad", "label": "family_role",' \
                ' "norm": "father", "gender": "male"}\n\n'
    my_fi = tmpdir.mkdir(pytest_temp).join("test_lexicon_map.txt")
    my_fi.write(dict_data)
    dict_dict, errors = fp.load_dict_from_jsonl(my_fi.strpath)
    assert len(dict_dict) == 2
    assert dict_dict['postdoc']['label'] == 'education_level'


def test_load_dict_from_jsonl_load_file(tmpdir):
    lex_data = '{"lemma": "origin", "label": "origin_term"}\n{"lemma": "born", "label": "origin_term"}\n'
    my_fi = tmpdir.mkdir(pytest_temp).join("test_lexicon_map.txt")
    my_fi.write(lex_data)
    dict_dict, errors = fp.load_dict_from_jsonl(my_fi.strpath)
    assert len(dict_dict) >= 2
    assert dict_dict['born']['label'] == 'origin_term'
