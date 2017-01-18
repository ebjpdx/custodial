import platform

from custodial import chrome_history, candidates, candidate_recommenders
from custodial.config import config


if platform.system() != 'Darwin':
    raise NotImplementedError('Only Mac is supported at this time')


chrome_history.make_local_copy(config)
urls = chrome_history.get_urls(config)
visits = chrome_history.get_visits(config)
freq_candidates = candidates.get(candidate_recommenders.by_usage_frequency)
# bookmarker.add(urls)

# Should I create classes, or remain functional?
