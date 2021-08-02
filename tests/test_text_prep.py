import pytest
from nlp_utils.preprocessor import Preprocessor

verbose = True


@pytest.fixture(scope='module')
def my_preppy():
    return Preprocessor()


# TODO: replace file and fix parsing
# @pytest.fixture(scope='module')
# def test_tweets():
#     test_inputs = []
#     # user_id, user_screen_name, user_lang, quill_lang, hashtag_texts, hashtags, content
#     with open('./data/quill_hashtag_metadata_lcmdb_FULL.txt') as csvfile:
#         tweet_reader = csv.reader(csvfile, delimiter='\t',  quotechar='"', lineterminator='\n')
#         lines_read = 0
#         for row in tweet_reader:
#             lines_read += 1
#             print("LENGTH", len(row))
#             print(row[4])
#             test_inputs.append(row[4])
#             if lines_read >= 100:
#                 break
#     return test_inputs
#
#
# def test_test_tweets(test_tweets):
#     for tweet in test_tweets:
#         print(tweet)


def test_normalize_tweet_keep_hashtags(my_preppy):
    tweet = " -- | Hey @friend I #love2live fast and free #blah #blah"
    result = my_preppy.normalize_tweet(tweet, hashtag2words=False)
    assert result == 'Hey @friend I #love2live fast and free'


def test_normalize_tweet_remove_rt(my_preppy):
    tweet = "RT @AndrewYang\nWant to help in Georgia? https://t.co/wM7bttCNqv sends money to 16 community orgs that " \
            "get out the vote! Who wants Mitch McConnell calling the shots - not me! We can help demote him on " \
            "January 5th in GA!\n "
    result = my_preppy.normalize_tweet(tweet, hashtag2words=False)
    assert result == 'Want to help in Georgia? https://t.co/wM7bttCNqv sends money to 16 community orgs that get out ' \
                     'the vote! Who wants Mitch McConnell calling the shots - not me! We can help demote him on ' \
                     'January 5th in GA!'


