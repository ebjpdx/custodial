from custodial.config import config
from custodial import chrome_history


def by_usage_frequency(min_weeks_observed=3):
    visits = chrome_history.get_visits(config)
    aggregation = {
        'visit_week': {
            'visit_count': 'count',
            'first_week_observed': 'min',
            'latest_week_observed': 'max'
        }
    }

    candidates = (
        visits[visits.weeks_observed >= min_weeks_observed]
        .groupby(['url', 'weeks_observed'])
        .agg(aggregation)
    )
    candidates.columns = candidates.columns.get_level_values(1)
    candidates = candidates[['first_week_observed', 'latest_week_observed', 'visit_count']]
    candidates.reset_index(inplace=True)
    candidates.set_index('url',inplace=True)
    candidates
    return candidates
