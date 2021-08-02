import csv
import json
import logging as log
import os
import pathlib
from pathlib import Path
from typing import Dict, List, Tuple
import unicodedata


def load_list(file_name, delim='\n', trim_elements=True) -> List[str]:
    """
    load a list from a file
    :param file_name: valid path to a file containing list items
    :param delim: a list delimiter.  Default is '\n', meaning one list element per line.
    :param trim_elements: bool indicating whether to remove space from the edges of individual list elements
    :return: a list of strings
    """
    the_list = []
    with open(file_name, "r", encoding="utf-8") as the_file:
        for cur_line in the_file:
            if cur_line:
                cur_line = cur_line.strip('\n')
                if delim == '\n':
                    if trim_elements:
                        cur_line = cur_line.strip()
                    the_list.append(cur_line)
                else:
                    line_list = cur_line.split(delim)
                    if line_list:
                        if trim_elements:
                            for element in line_list:
                                the_list.append(element.strip())
                        else:
                            the_list.extend(line_list)
    return the_list


def load_dict(file_name, delim='|',
              norm_keys: bool = True,
              norm_values: bool = True,
              key_col: int = 1,
              val_col: int = 2,
              max_errs: int = 5) -> Tuple[Dict, List[str]]:
    """
    load a dict from a file
    :param file_name: valid path to a file containing list items
    :param delim: a list delimiter.  Default is '|', the pipe character
    :param norm_keys: bool indicating whether to unicode normalize and lowercase keys in the returned dictionary
    :param norm_values: bool indicating whether to unicode normalize values in the returned dictionary
    :param key_col:  int indicating the column in which to find dictionary keys, 1 is the first column number
    :param val_col:  int indicating the column in which to find dictionary values, 1 is the first column number
    :param max_errs: int
    :return: a list
    """
    the_dict = {}
    errors = []
    if key_col < 1:
        errors.append(f"{0}|invalid column for key_col: {key_col}")
    if val_col < 1:
        errors.append(f"{0}|invalid column for val_col: {val_col}")
    if errors:
        return the_dict, errors

    key_col = key_col - 1
    val_col = val_col - 1
    with open(file_name, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        line_num = 0
        for cur_line in csv_reader:
            line_num += 1
            line_len = len(cur_line)
            if len(errors) >= max_errs:
                break
            if key_col >= line_len or val_col >= line_len:
                if key_col >= line_len:
                    errors.append(f"{line_num}|key column index {key_col} out of bounds for row len: {line_len}")
                if val_col >= line_len:
                    errors.append(f"{line_num}|value column index {val_col} out of bounds for row len: {line_len}")
                continue
            the_key = cur_line[key_col].strip()
            the_val = cur_line[val_col].strip()
            if norm_keys:
                the_key = unicodedata.normalize('NFKD', the_key.lower())
            if norm_values:
                the_val = unicodedata.normalize('NFKD', the_val)
            if the_key not in the_dict.keys():
                the_dict[the_key] = the_val
    return the_dict, errors


#  TODO: do a better job at dictionary loading, merge this method with the load_dict method of this file

def load_dictionary(lang_dir, dictionary_file, has_header=True):

    if not os.path.isfile(dictionary_file):
        dictionary_rsc = os.path.join(pathlib.Path(__file__).parent, '', 'data', lang_dir, dictionary_file)
        if not os.path.isfile(dictionary_rsc):
            log.warning(f"File not: neither {dictionary_file} nor {dictionary_rsc}")
            return None
        dictionary_file = dictionary_rsc
    dictionary = {}
    try:
        with open(dictionary_file, "r", encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                if has_header and line_count == 0:
                    log.debug(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    key = row[0].strip().lower()
                    if key not in dictionary.keys():
                        the_rest = row[1:len(row)]
                        if not the_rest:
                            the_rest = ''
                        dictionary[key] = the_rest
                line_count += 1
            log.debug(f'Loaded {line_count} dictionary entries.')
    except Exception as eek:
        log.error(eek)
    return dictionary


def load_dict_from_csv(file_name,
                       delim = '|',
                       norm_keys: bool = True,
                       norm_values: bool = True,
                       key_col: int = 1,
                       val_col: int = 2,
                       max_errs: int = -1) -> Tuple[dict, List[str]]:
    """
    load a dict from a file
    :param file_name: valid path to a file containing the dict entries
    :param delim: character to use as a column delimiter
    :param norm_keys: bool indicating whether to unicode normalize and lowercase keys in the returned dictionary
    :param norm_values: bool indicating whether to unicode normalize values in the returned dictionary
    :param key_col:  int indicating the column in which to find dictionary keys, 1 is the first column number
    :param val_col:  int indicating the column in which to find dictionary values, 1 is the first column number
    :param max_errs: int
    :return: a list
    """
    the_dict = {}
    errors: List[str] = []
    if key_col < 1:
        errors.append(f"{0}|invalid column for key_col: {key_col}")
    if val_col < 1:
        errors.append(f"{0}|invalid column for val_col: {val_col}")
    if errors:
        return the_dict, errors

    key_col = key_col - 1
    val_col = val_col - 1
    with open(file_name, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        line_num = 0
        for cur_line in csv_reader:
            line_num += 1
            line_len = len(cur_line)
            if max_errs != -1 and len(errors) >= max_errs:
                break
            if key_col >= line_len or val_col >= line_len:
                if key_col >= line_len:
                    errors.append(f"{line_num}|key column index {key_col} out of bounds for row len: {line_len}")
                if val_col >= line_len:
                    errors.append(f"{line_num}|value column index {val_col} out of bounds for row len: {line_len}")
                continue
            the_key = cur_line[key_col].strip()
            the_val = cur_line[val_col].strip()
            if norm_keys:
                the_key = unicodedata.normalize('NFKD', the_key.lower())
            if norm_values:
                the_val = unicodedata.normalize('NFKD', the_val)
            if the_key not in the_dict.keys():
                the_dict[the_key] = the_val
            if max_errs != -1 and len(errors) >= max_errs:
                break
    return the_dict, errors


# TODO: add error checking to get_project_root
def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def find_file(file_name, paths_to_search=None):
    if not paths_to_search:
        paths_to_search = [get_project_root()]
    files_found = []
    for cur_dir in paths_to_search:
        # if '~' in cur_dir:
        #     cur_dir = os.path.expanduser(cur_dir)
        for path, sub_dirs, files in os.walk(cur_dir):
            for name in files:
                if file_name == name:
                    file_path = os.path.join(path, name)
                    files_found.append(file_path)
    return files_found


def load_dict_from_jsonl(lexicon_file, key_field='lemma', error_limit=-1):
    the_dict = {}
    errors = []
    if not os.path.isfile(lexicon_file):
        lexicon_file_list = find_file(lexicon_file)
        if lexicon_file_list and len(lexicon_file_list) == 1:
            lexicon_file = lexicon_file_list[0]
        else:
            errors.append(f"lexicon file not located: {lexicon_file}")
    if lexicon_file:
        with open(lexicon_file, "r", encoding="utf8") as jsonl_file:
            line_count = 0
            for entry in jsonl_file:
                line_count += 1
                entry = entry.strip()
                if not entry:
                    continue
                try:
                    entry_dict = json.loads(entry.strip())
                    if key_field in entry_dict.keys():
                        the_dict[entry_dict[key_field]] = entry_dict
                    else:
                        errors.append(f"line {line_count}, key not found: {key_field}")
                except IOError as ioEek:
                    errors.append(f"line {line_count}, error reading JSON: {ioEek}")
                except ValueError as valEek:
                    errors.append(f"line {line_count}, error reading JSON: {valEek}")
                if error_limit != -1 and len(errors) >= error_limit:
                    break
    return the_dict, errors
