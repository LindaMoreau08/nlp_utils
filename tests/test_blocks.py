# -*- coding: utf-8 -*-

import nlp_utils.unicode_blocks as blocks


def test_basic_latin():
    test_char = 'a'
    assert blocks.block(test_char) == 'Basic Latin'


def test_cyrillic():
    test_char = 'а'
    assert blocks.block(test_char) == 'Cyrillic'
