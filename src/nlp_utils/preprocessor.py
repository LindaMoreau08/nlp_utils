import inspect
import regex
import unicodedata

import nlp_utils.file_parsers as fp
import nlp_utils.string_utils as su
import nlp_utils.simple_tokenizer as token_tests


class Preprocessor:

    def __init__(self, lang='eng'):
        self.known_words = None

    @staticmethod
    def tokenize(text):
        """
        a quick heuristic token split
        """
        if text is None:
            return text
        cheap_tokens = text.split()
        tokens = []
        for c_token in cheap_tokens:
            if len(c_token) >= 2 and c_token[-1] in "?!.-" and c_token[-2] not in "?!.-" :
                tokens.append(c_token[0: len(c_token) - 1])
                tokens.append(c_token[-1])
            else:
                tokens.append(c_token)
        return tokens

    def __load_resources(self, lang='eng'):
        self.known_words = fp.load_dictionary(lang, 'eng_word_list.csv', has_header=False)


    @staticmethod
    def __trim_tweet(tweet_text):

        if tweet_text is None:
            return tweet_text
        cheap_tokens = tweet_text.split()
        token_index = len(cheap_tokens) - 1
        while token_index >= 0:
            cur_token = cheap_tokens[token_index]
            if Preprocessor.__should_remove(cur_token):
                del cheap_tokens[token_index]
            else:
                break
            token_index -= 1
        tweet_text = ' '.join(cheap_tokens)
        return tweet_text

    def __hashtag_to_words(self, tweet_text):
        if tweet_text is None:
            return tweet_text
        temp_tokens = []
        tweet_tokens = self.tokenize(tweet_text)
        for token in tweet_tokens:
            if len(token) < 1:
                continue
            if token[0] == '#':
                token = self.hashtag2word(token)
            temp_tokens.append(token)
        tweet = ' '.join(temp_tokens)
        return tweet

    @staticmethod
    def __should_remove(token):
        if token_tests.is_url(token):
            return True
        if token_tests.is_hashtag(token):
            return True
        return False

    def hashtag2word(self, hashtag, lowercase=True):
        nonhashtag = hashtag.strip('#@ ')
        word = self.check_word(nonhashtag)
        if word:
            return word
        hashtag_tokens = regex.split("[_.@/-]", nonhashtag)
        new_tokens = []
        for hash_tok in hashtag_tokens:
            word = self.check_word(hash_tok)
            if word:
                new_tokens.append(word)
            else:
                word = self.recover_words(hash_tok)
                if word:
                    new_tokens.append(word)
                else:
                    new_tokens.append(hash_tok)
        recovered_words = ' '.join(new_tokens)
        if lowercase:
            recovered_words = recovered_words.lower()
        return recovered_words

    def recover_words(self, text, lowercase=True):
        # TODO: must deal with number tokens
        parts = su.split_by_category(text)
        new_tokens = []
        for part in parts:
            word = self.check_word(part)
            if word:
                new_tokens.append(word)
            else:
                return None
        recovered_words = ' '.join(new_tokens)
        if lowercase:
            recovered_words = recovered_words.lower()
        return recovered_words

    def check_word(self, word_candidate):
        transforms = [su.norm_for_word_recovery, su.norm_for_word_recovery, su.dediacritize]
        transform_step = 0
        for transform in transforms:
            sig = inspect.signature(transform)
            if transform_step > 0 and 'allow_two_repeats' in sig.parameters.keys():
                word_candidate = transform(word_candidate, allow_two_repeats=False)
            else:
                word_candidate = transform(word_candidate)
            if self.is_known_word(word_candidate):
                return word_candidate
            transform_step += 1

        return None

    def is_known_word(self, word):
        """
        determine whether this is a known word from our inflected word list
        @param word: the word to assess
        @return: true if the word is in our known words list, false otherwise
        """
        if word is not None and self.known_words is not None:
            word = word.strip().lower()
            word = regex.sub(r"[\s\t\n\p{Z}_-]+", " ", word)
            word = word.strip()
            if word in self.known_words.keys():
                return True
            if len(word) >= 2 and word[-1] == 's' and word[-2] != 's':
                word = word.lstrip('s')
                if word in self.known_words.keys():
                    return True
        return False

    def normalize_tweet(self, tweet, to_lower=False, trim_edges=True, hashtag2words=False):
        """
        @param tweet: the content of the Tweet to be normalized
        @param to_lower: whether or not to lowercase the tweet
        @param trim_edges: whether to remove edge materials, e.g. urls, hashtags, @mentions, selected punctuation
        @param hashtag2words: whether to attempt to recover words from hashtags
        @return: a string representing a normalized tweet
        """
        if tweet is None:
            return tweet
        tweet = tweet.strip(' -|\n\r')
        tweet = unicodedata.normalize('NFKD', tweet)
        a_match = regex.match(r"^rt[:\s-]*@[^\s]+[\s\n\|\-]+", tweet, regex.IGNORECASE)
        if a_match:
            tweet = tweet[a_match.end():]
        if to_lower:
            tweet = tweet.lower()
        tweet = regex.sub(r"\s-+\s*\|?", " - ", tweet)  #TODO: see if this is redundant
        tweet = regex.sub(r"[\s\t\n\p{Z}]+", ' ', tweet)
        if trim_edges:
            tweet = self.__trim_tweet(tweet)
        if hashtag2words:
            tweet = self.__hashtag_to_words(tweet)
        return tweet

# TODO: try a trie? or an icu-style tokenizer for single case items with no obvious word breaks


