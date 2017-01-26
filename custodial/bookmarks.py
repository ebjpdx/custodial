import pandas as pd

from custodial.config import conn
from custodial import metadata
from sqlalchemy.sql import bindparam


def current():
    return pd.read_sql(
        sql='select * from bookmarks',
        con=conn,
        index_col='url'
    )


def append(cnd):
    current_bookmarks = current()
    current_bookmarks.latest_week_observed = pd.to_datetime(current_bookmarks.latest_week_observed)

    # Update dates on current bookmarks
    existing_urls = cnd.join(current_bookmarks[['latest_week_observed']], how='inner', rsuffix='_new')
    existing_urls = existing_urls[existing_urls.latest_week_observed != existing_urls.latest_week_observed_new]

    if (existing_urls.shape[0] > 0):
        updt = (metadata.bookmarks.update()
                .where(metadata.bookmarks.c.url == bindparam('s_url'))
                .values(latest_week_observed=bindparam('latest_week_observed'))
                )
        existing_urls.index.rename('s_url', inplace=True)  # Changing name because sqlalchemy reserves column names
        records_to_change = existing_urls.reset_index()[['s_url', 'latest_week_observed']].to_dict('records')

        conn.execute(updt, records_to_change)

    # Insert new URLs
    idx_new_urls = cnd.index.difference(current_bookmarks.index)
    (cnd
     .loc[idx_new_urls][['first_week_observed', 'latest_week_observed', 'weeks_observed']]
     .to_sql('bookmarks', conn, if_exists='append')
     )
