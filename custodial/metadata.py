import datetime

from sqlalchemy import Table, Column, Integer, String, Date, DateTime, MetaData
from sqlalchemy.sql import func

metadata = MetaData()

bookmarks = Table('bookmarks', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('url', String, nullable=False),
                  Column('first_week_observed', Date),
                  Column('latest_week_observed', Date),
                  Column('weeks_observed', Integer),
                  Column('created_at', DateTime, server_default=func.now()),
                  Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                  )

bookmark_exclusions = Table('bookmark_exclusions', metadata,
                            Column('url_pattern', String, primary_key=True),
                            Column('pattern_type', String, nullable=False),
                            Column('created_at', DateTime, server_default=func.now()),
                            Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                            )
