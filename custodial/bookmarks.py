import pandas as pd

from custodial.config import conn, config
# from custodial import chrome_history, metadata


def current():
    pd.read_sql(
        sql='select * from bookmarks',
        con=conn,
        index_col='id'
    )

