import nlp_utils.unicode_blocks as blocks


# get the most likely writing system of a text
def writing_system(text):
    all_scripts = script_profile(text)
    all_scripts_simple = remove_common(all_scripts)
    if len(all_scripts_simple) == 1:
        return all_scripts_simple[0][0]
    is_all_han = all_han(all_scripts)
    if is_all_han: return 'Han'
    is_all_japanese = all_japanese(all_scripts)
    if is_all_japanese: return 'Japanese'
    is_all_korean = all_korean(all_scripts)
    if is_all_korean: return 'Korean'
    is_all_chinese = all_chinese(all_scripts)
    if is_all_chinese: return 'Chinese'
    # TO DO:  better heuristic for mixed language after this point
    return all_scripts[0][0]


def remove_common(profile):
    simple_profile = []
    for cur_tuple in profile:
        if cur_tuple[0] in ['Inherited', 'Common', 'Symbol']:
            continue
        else:
            simple_profile.append(cur_tuple)
    return simple_profile


def find_cyrillic(text, return_chars=False):
    import regex
    pattern = regex.compile(r'\p{Cyrillic}')
    matches = pattern.findall(text)
    if matches:
        if return_chars:
            return matches
        else:
            return len(matches)
    if return_chars:
        return []
    return 0


def all_han(profile):
    return all_script_or_common(profile, ['Han'])


# given a script profile, determine if all scripts are Japanese compatible
def all_japanese(profile):
    return all_script_or_common(profile, ['Hiragana', 'Katakana', 'Han'])


# given a script profile, determine if all scripts are Japanese compatible
def all_chinese(profile):
    return all_script_or_common(profile, ['Bopomofo', 'Han'])


# given a script profile, determine if all scripts are Japanese compatible
def all_korean(profile):
    return all_script_or_common(profile, ['Hangul', 'Han'])


def all_script_or_common(profile, script_list):
    has_lang = False
    for profile_script in profile:
        if profile_script[0] in script_list:
            has_lang = True
        elif profile_script[0] in ['Common', 'Inherited', 'Symbols', 'Latin']:
            continue
        else:
            return False
    return has_lang


def script_profile(text):
    text_scripts = {}
    for cur_char in text:
        cur_script = script_re(cur_char)
        if cur_script in text_scripts:
            text_scripts[cur_script] += 1
        else:
            text_scripts[cur_script] = 1
    return sort_profile(text_scripts)


def script_profile_blocks(text):
    text_scripts = {}
    for cur_char in text:
        cur_block = blocks.block(cur_char)
        cur_script = script(cur_block)
        if cur_script in text_scripts:
            text_scripts[cur_script] += 1
        else:
            text_scripts[cur_script] = 1
    return sort_profile(text_scripts)


def sort_profile(profile):
    import operator
    if profile:
        return sorted(profile.items(), key=operator.itemgetter(1), reverse=True)
    return profile


def script_re(ch):
    import regex
    for cur_regex in _scriptRegexes:
        reguex = "^" + cur_regex + "$"
        m = regex.match(reguex, ch)
        if m:
            return _scriptRegexes[cur_regex]
    return 'unknown'


def script(block_name):
    if block_name in _scripts:
        return _scripts[block_name]
    return 'unknown'


def _initScripts(text):
    global _scripts
    _scripts = {}
    for line in text.split('\n'):
        if not line or 'BLOCK' in line:
            continue
        columns = line.split(';')
        new_block = columns[0]
        new_script = columns[1]
        new_block = new_block.strip()
        new_script = new_script.strip()
        _scripts[new_block] = new_script


_initScripts('''
BLOCK; SCRIPT
Adlam; Adlam
Aegean Numbers; Aegean
Ahom; Ahom
Alphabetic Presentation Forms; Alphabetic_Presentation_Forms
Enclosed Alphanumeric Supplement; Alphanumeric
Enclosed Alphanumerics; Alphanumeric
Old North Arabian; Arabian
Old South Arabian; Arabian
Arabic; Arabic
Arabic Extended-A; Arabic
Arabic Mathematical Alphabetic Symbols; Arabic
Arabic Presentation Forms-A; Arabic
Arabic Presentation Forms-B; Arabic
Arabic Supplement; Arabic
Imperial Aramaic; Aramaic
Armenian; Armenian
Arrows; Arrows
Supplemental Arrows-A; Arrows
Supplemental Arrows-B; Arrows
Supplemental Arrows-C; Arrows
Avestan; Avestan
Balinese; Balinese
Bamum; Bamum
Bamum Supplement; Bamum
Bassa Vah; Bassa_Vah
Batak; Batak
Bengali; Bengali
Bhaiksuki; Bhaiksuki
Brahmi; Brahmi
Braille Patterns; Braille
Buginese; Buginese
Buhid; Buhid
Unified Canadian Aboriginal Syllabics; Canadian_Aboriginal
Unified Canadian Aboriginal Syllabics Extended; Canadian_Aboriginal
Carian; Carian
Caucasian Albanian; Caucasian_Albanian
Chakma; Chakma
Cham; Cham
Cherokee; Cherokee
Cherokee Supplement; Cherokee
Bopomofo; CJK
Bopomofo Extended; CJK
CJK Compatibility; CJK
CJK Compatibility Forms; CJK
CJK Compatibility Ideographs; CJK
CJK Compatibility Ideographs Supplement; CJK
CJK Radicals Supplement; CJK
CJK Strokes; CJK
CJK Symbols and Punctuation; CJK
CJK Unified Ideographs; CJK
CJK Unified Ideographs Extension A; CJK
CJK Unified Ideographs Extension B; CJK
CJK Unified Ideographs Extension C; CJK
CJK Unified Ideographs Extension D; CJK
CJK Unified Ideographs Extension E; CJK
CJK Unified Ideographs Extension F; CJK
Enclosed CJK Letters and Months; CJK
Enclosed Ideographic Supplement; CJK
Halfwidth and Fullwidth Forms; CJK
Ideographic Description Characters; CJK
Ideographic Symbols and Punctuation; CJK
Kangxi Radicals; CJK
Small Form Variants; CJK
Vertical Forms; CJK
Coptic; Coptic
Coptic Epact Numbers; Coptic
Cuneiform; Cuneiform
Cuneiform Numbers and Punctuation; Cuneiform
Early Dynastic Cuneiform; Cuneiform
Currency Symbols; Currency
Cypriot Syllabary; Cypriot
Cyrillic; Cyrillic
Cyrillic Extended-A; Cyrillic
Cyrillic Extended-B; Cyrillic
Cyrillic Extended-C; Cyrillic
Cyrillic Supplement; Cyrillic
Deseret; Deseret
Devanagari; Devanagari
Devanagari Extended; Devanagari
Combining Diacritical Marks; Diacritic
Combining Diacritical Marks Extended; Diacritic
Combining Diacritical Marks for Symbols; Diacritic
Combining Diacritical Marks Supplement; Diacritic
Combining Half Marks; Diacritic
Modifier Tone Letters; Diacritic
Spacing Modifier Letters; Diacritic
Variation Selectors Supplement; Diacritic
Dogra; Dogra
Duployan; Duployan
Elbasan; Elbasan
Elymaic; Elymaic
Emoticons; Emoticons
Ethiopic; Ethiopic
Ethiopic Extended; Ethiopic
Ethiopic Extended-A; Ethiopic
Ethiopic Supplement; Ethiopic
Shorthand Format Controls; Format
Chess Symbols; Game
Domino Tiles; Game
Mahjong Tiles; Game
Playing Cards; Game
Georgian; Georgian
Georgian Extended; Georgian
Georgian Supplement; Georgian
Glagolitic; Glagolitic
Glagolitic Supplement; Glagolitic
Gothic; Gothic
Grantha; Grantha
Ancient Greek Musical Notation; Greek
Ancient Greek Numbers; Greek
Greek and Coptic; Greek
Greek Extended; Greek
Gujarati; Gujarati
Gunjala Gondi; Gunjala_Gondi
Gurmukhi; Gurmukhi
Hanunoo; Hanunoo
Hatran; Hatran
Hebrew; Hebrew
Anatolian Hieroglyphs; Hieroglyph
Egyptian Hieroglyph Format Controls; Hieroglyph
Egyptian Hieroglyphs; Hieroglyph
Meroitic Hieroglyphs; Hieroglyph
Nyiakeng Puachue Hmong; Hmong
Pahawh Hmong; Hmong
Old Hungarian; Hungarian
Common Indic Number Forms; Indic
Old Italic; Italic
Hiragana; Japanese
Kana Extended-A; Japanese
Kana Supplement; Japanese
Katakana; Japanese
Katakana Phonetic Extensions; Japanese
Small Kana Extension; Japanese
Javanese; Javanese
Kaithi; Kaithi
Kanbun; Kanbun
Kannada; Kannada
Kayah Li; KayahLi
Kharoshthi; Kharoshthi
Khmer; Khmer
Khmer Symbols; Khmer
Khojki; Khojki
Khudawadi; Khudawadi
Hangul Compatibility Jamo; Korean
Hangul Jamo; Korean
Hangul Jamo Extended-A; Korean
Hangul Jamo Extended-B; Korean
Hangul Syllables; Korean
Lao; Lao
Basic Latin; Latin
Latin Extended Additional; Latin
Latin Extended-A; Latin
Latin Extended-B; Latin
Latin Extended-C; Latin
Latin Extended-D; Latin
Latin Extended-E; Latin
Latin-1 Supplement; Latin
Letterlike Symbols; Latin
Superscripts and Subscripts; Latin
Lepcha; Lepcha
Limbu; Limbu
Linear A; Linear
Linear B Ideograms; Linear
Linear B Syllabary; Linear
Lisu; Lisu
Lycian; Lycian
Lydian; Lydian
Mahajani; Mahajani
Makasar; Makasar
Malayalam; Malayalam
Mandaic; Mandaic
Manichaean; Manichaean
Marchen; Marchen
Masaram Gondi; Masaram_Gondi
Counting Rod Numerals; Mathematical
Mathematical Alphanumeric Symbols; Mathematical
Mathematical Operators; Mathematical
Miscellaneous Mathematical Symbols-A; Mathematical
Miscellaneous Mathematical Symbols-B; Mathematical
Supplemental Mathematical Operators; Mathematical
Mayan Numerals; Mayan
Medefaidrin; Medefaidrin
Meetei Mayek; Meetei_Mayek
Meetei Mayek Extensions; Meetei_Mayek
Mende Kikakui; Mende_Kikakui
Meroitic Cursive; Meroitic
Miao; Miao
Modi; Modi
Mongolian; Mongolian
Mongolian Supplement; Mongolian
Mro; Mro
Multani; Multani
Byzantine Musical Symbols; Musical
Musical Symbols; Musical
Myanmar; Myanmar
Myanmar Extended-A; Myanmar
Myanmar Extended-B; Myanmar
Nabataean; Nabataean
Nandinagari; Nandinagari
New Tai Lue; New_Tai_Lue
Newa; Newa
NKo; NKo
Number Forms; Number
Nushu; Nushu
Optical Character Recognition; OCR
Ogham; Ogham
Ol Chiki; Ol_Chiki
Oriya; Oriya
Osage; Osage
Osmanya; Osmanya
Inscriptional Pahlavi; Pahlavi
Psalter Pahlavi; Pahlavi
Palmyrene; Palmyrene
Inscriptional Parthian; Parthian
Pau Cin Hau; Pau_Cin_Hau
Old Permic; Permic
Old Persian; Persian
Phags-pa; Phags-pa
Phaistos Disc; Phaistos_Disc
Phoenician; Phoenician
IPA Extensions; Phonetic
Phonetic Extensions; Phonetic
Phonetic Extensions Supplement; Phonetic
High Private Use Surrogates; Private
Private Use Area; Private
Supplementary Private Use Area-A; Private
Supplementary Private Use Area-B; Private
General Punctuation; Punctuation
Supplemental Punctuation; Punctuation
Rejang; Rejang
Hanifi Rohingya; Rohingya
Rumi Numeral Symbols; Rumi
Runic; Runic
Samaritan; Samaritan
Saurashtra; Saurashtra
Sharada; Sharada
Shavian; Shavian
Siddham; Siddham
Sinhala; Sinhala
Sinhala Archaic Numbers; Sinhala
Indic Siyaq Numbers; Siyaq
Ottoman Siyaq Numbers; Siyaq
Old Sogdian; Sogdian
Sogdian; Sogdian
Sora Sompeng; Sora_Sompeng
Soyombo; Soyombo
Specials; Specials
Sundanese; Sundanese
Sundanese Supplement; Sundanese
High Surrogates; Surrogate
Low Surrogates; Surrogates
Sutton SignWriting; Sutton
Syloti Nagri; Syloti_Nagri
Dingbats; Symbol
Ornamental Dingbats; Symbol
Alchemical Symbols; Symbols
Ancient Symbols; Symbols
Block Elements; Symbols
Box Drawing; Symbols
Control Pictures; Symbols
Geometric Shapes; Symbols
Geometric Shapes Extended; Symbols
Miscellaneous Symbols; Symbols
Miscellaneous Symbols and Arrows; Symbols
Miscellaneous Symbols and Pictographs; Symbols
Miscellaneous Technical; Symbols
Supplemental Symbols and Pictographs; Symbols
Symbols and Pictographs Extended-A; Symbols
Transport and Map Symbols; Symbols
Syriac; Syriac
Syriac Supplement; Syriac
Tagalog; Tagalog
Tagbanwa; Tagbanwa
Tags; Tags
Tai Le; Tai_Le
Tai Tham; Tai_Tham
Tai Viet; Tai_Viet
Tai Xuan Jing Symbols; Tai_Xuan_Jing
Takri; Takri
Tamil; Tamil
Tamil Supplement; Tamil
Tangut; Tangut
Tangut Components; Tangut
Telugu; Telugu
Thaana; Thaana
Thai; Thai
Tibetan; Tibetan
Tifinagh; Tifinagh
Tirhuta; Tirhuta
Old Turkic; Turkic
Ugaritic; Ugaritic
Vai; Vai
Variation Selectors; Vai
Vedic Extensions; Vedic
Wancho; Wancho
Warang Citi; Warang_Citi
Yi Radicals; Yi
Yi Syllables; Yi
Yijing Hexagram Symbols; Yijing
Zanabazar Square; Zanabazar_Square
''')


def _initScriptRegexes(regexes):
    global _scriptRegexes
    _scriptRegexes = {}
    for line in regexes.split('\n'):
        if not line:
            continue
        script_rgx = line
        script_rgx.strip()
        script_name = script_rgx
        script_name = script_name.replace("\\p{", "")
        script_name = script_name.replace("}", "")
        script_name = script_name.strip()
        _scriptRegexes[script_rgx] = script_name


_initScriptRegexes(r'''
\p{Common}
\p{Inherited}
\p{Latin}
\p{Cyrillic}
\p{Arabic}
\p{Hebrew}
\p{Han}
\p{Hiragana}
\p{Katakana}
\p{Hangul}
\p{Bopomofo}
\p{Armenian}
\p{Greek}
\p{Georgian}
\p{Bengali}
\p{Devanagari}
\p{Thai}
\p{Gujarati}
\p{Gurmukhi}
\p{Kannada}
\p{Malayalam}
\p{Sinhala}
\p{Tamil}
\p{Telugu}
\p{Thaana}
\p{Tibetan}
\p{Lao}
\p{Mongolian}
\p{Myanmar}
\p{Ethiopic}
\p{Tagalog}
\p{Oriya}
\p{Khmer}
\p{Buhid}
\p{Canadian_Aboriginal}
\p{TaiLe}
\p{Limbu}
\p{Ogham}
\p{Runic}
\p{Syriac}
\p{Tagbanwa}
\p{Hanunoo}
\p{Cherokee}
\p{Braille}
''')
