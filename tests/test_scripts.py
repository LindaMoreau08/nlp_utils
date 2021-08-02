import nlp_utils.unicode_scripts as scripts
debug = True


def test_script_profile():
    input = 'this is a test  ذيس إس أ اختبار   这是一个测验 123'
    actual = scripts.script_profile(input)
    if debug:
        print('\n')
        for script_count in actual:
            print(script_count)
    assert actual == [('Common', 15), ('Arabic', 12), ('Latin', 11), ('Han', 6)]


def test_script_profile_cjk():
    text = '量子コンピュータだけでない！！ あらゆる分野が著しく衰退しとる！！'
    actual = scripts.script_profile(text)
    if debug:
        print('\n')
        for script_count in actual:
            print(script_count)
    assert actual == [('Hiragana', 15), ('Han', 7), ('Common', 6), ('Katakana', 5 )]


def test_writing_systemk():
    text = '量子コンピュータだけでない！！ あらゆる分野が著しく衰退しとる！！'
    actual = scripts.writing_system(text)
    if debug:  print('\n'+actual)
    assert actual == 'Japanese'


def test_num_cyrillic():
    text = 'роасh'
    actual = scripts.find_cyrillic(text,False)
    assert actual == 4
    text = 'poach'
    actual = scripts.find_cyrillic(text,False)
    assert actual == 0


#'새끼 고양이 가족을 찾아요🐱'
