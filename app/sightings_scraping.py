import snscrape.modules.twitter as sntwitter
import re
import json
from pathlib import Path

with open(Path('app','bird_names.json'), 'r') as f:
    unformatted_bird_names = json.load(f)

BIRD_NAMES = {re.sub('[^\w ]', '', k).lower(): v for k,v in unformatted_bird_names.items()}

def get_sightings(
    req
):

    keyword = req['keyword']
    maxTweets = req['max_tweets']
    start_date_str = req['start_date']
    end_date_str = req['end_date']

    search_str = re.compile("\\b({})s?\\b".format(
        '|'.join(BIRD_NAMES.keys())
    ))

    recs = []
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(
            f'{keyword} -(from:otmoormr) since:{start_date_str} until:{end_date_str}'
        ).get_items()
    ):
        if i > maxTweets:
            break
        rec = {
            'id': str(tweet.id),
            'date': tweet.date,
            'content': tweet.content,
            'content_clean': re.sub('\s+',' ',re.sub('[^\w\s@#]','', tweet.content)).lower()
        }
        rec['birds'] = re.findall(search_str, rec['content_clean'])
        rec['birds'] = [BIRD_NAMES[name] for name in rec['birds']]
        if rec['birds']:
            recs.append(rec)

    return recs