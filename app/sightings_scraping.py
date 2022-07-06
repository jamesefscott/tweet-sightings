import snscrape.modules.twitter as sntwitter
import re
import json
from pathlib import Path

# with open(Path('app','bird_names.json'), 'r') as f:
#     unformatted_bird_names = json.load(f)
# with open(Path('app','butterfly_names.json'), 'r') as f:
#     unformatted_butterfly_names = json.load(f)
with open(Path('app','all_species_data.json'), 'r') as f:
    all_species_data = json.load(f)

# BIRD_NAMES = {re.sub('[^\w ]', '', k).lower(): v for k,v in unformatted_bird_names.items()}
# BUTTERFLY_NAMES = {re.sub('[^\w ]', '', k).lower(): v for k,v in unformatted_butterfly_names.items()}
ALL_SPECIES = {re.sub('[^\w ]', '', sp).lower(): sp for sp in all_species_data.keys()}

GROUP_CONDITIONS = {
    'Birds': {'tx_level': 'Class',
              'tx_list': ['Aves']},
    'Lepidoptera': {'tx_level': 'Order',
                    'tx_list': ['Lepidoptera']},
    'Other Animals': {'tx_level': 'Kingdom',
            'tx_list': ['Animalia']},
    'Plants': {'tx_level': 'Kingdom',
            'tx_list': ['Plantae']},
    'Fungi': {'tx_level': 'Kingdom',
            'tx_list': ['Fungi']}
}


def check_group_conditions(common_name):
    for label, gc in GROUP_CONDITIONS.items():
        if all_species_data[common_name][gc['tx_level']] in gc['tx_list']:
            return label
    return 'Hmm'


def get_sightings(
    req
):

    keyword = req['keyword']
    maxTweets = req['max_tweets']
    start_date_str = req['start_date']
    end_date_str = req['end_date']

    search_str = re.compile("\\b({})s?\\b".format(
        '|'.join(ALL_SPECIES.keys())
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
        rec['species'] = re.findall(search_str, rec['content_clean'])
        rec['species'] = [ALL_SPECIES[name] for name in rec['species']]
        rec['labels'] = [check_group_conditions(sp) for sp in rec['species']]

        if rec['species']:
            recs.append(rec)

    return recs